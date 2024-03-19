import { Component, OnDestroy, OnInit } from '@angular/core';
import { PostContentComponent } from '../post-content/post-content.component';
import { Post } from '../../models/interfaces/post.interface';
import { PostService } from '../../services/post.service';
import { CommonModule } from '@angular/common';
import { LikeCounterComponent } from '../like-counter/like-counter.component';
import { CommentCounterComponent } from '../comment-counter/comment-counter.component';
import { LikeService } from '../../services/like.service';
import { CommentService } from '../../services/comment.service';
import { AuthService } from '../../services/auth.service';
import { UserStateService } from '../../services/user-state.service';
import { LikeActionComponent } from '../like-action/like-action.component';
import { DeleteActionComponent } from '../delete-action/delete-action.component';
import { CommentActionComponent } from '../comment-action/comment-action.component';
import { EditActionComponent } from '../edit-action/edit-action.component';
import { Category } from '../../models/enums/category.enum';
import { Permission } from '../../models/enums/permission.enum';
import { User } from '../../models/interfaces/user.interface';
import { MatDialog } from '@angular/material/dialog';
import { PostDeleteDialogComponent } from '../post-delete-dialog/post-delete-dialog.component';
import { NavigationExtras, Router } from '@angular/router';

@Component({
  selector: 'app-post-list',
  standalone: true,
  imports: [
    PostContentComponent,
    LikeCounterComponent,
    CommentCounterComponent,
    LikeActionComponent,
    CommentActionComponent,
    EditActionComponent,
    DeleteActionComponent,
    CommonModule,
  ],
  templateUrl: './post-list.component.html',
  styleUrl: './post-list.component.sass',
})
export class PostListComponent implements OnInit {
  posts!: Post[];
  isAuthenticated = false;

  constructor(
    private postService: PostService,
    private likeService: LikeService,
    private commentService: CommentService,
    private authService: AuthService,
    private userService: UserStateService,
    private dialog: MatDialog
  ) {}

  ngOnInit() {
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isAuthenticated = isAuthenticated;
    });
    this.fetchData();
  }

  fetchData(): void {
    this.postService.list().subscribe((posts) => {
      this.posts = posts;
      this.getLikedByUser();
      this.getLikes();
      this.getComments();
      this.setPermissions();
    });
  }

  handleLikeAction(isLiked: boolean, postId: number): void {
    const currentPostIndex = this.posts.findIndex((post) => post.id === postId);
    const currentPost = {...this.posts[currentPostIndex]};
    const user = this.userService.getUser();
    if (isLiked) {
      this.handleDeleteLike(currentPost, user.id);
    } else {
      this.handleCreateLike(currentPost, user);
    }
    this.posts[currentPostIndex] = currentPost;
  }

  handleDeleteLike(currentPost: Post, userId: number): void {
    this.likeService.deleteLike(currentPost.id, userId).subscribe({
      next: () => {},
      error: (error) => {console.error(error)}
    });
    // Render UI optimistically
    currentPost.likes!.count--;
    currentPost.likes!.likedBy = currentPost.likes!.likedBy.filter(obj => obj.id !== userId);
    currentPost.likedByAuthenticatedUser = false;
  }

  handleCreateLike(currentPost: Post, user: User): void {
    this.likeService.createLike(currentPost.id, user.id).subscribe({
      next: () => {},
      error: (error) => {console.error(error)}
    });
    // Render UI optimistically
    currentPost.likes!.count++;
    currentPost.likes!.likedBy.unshift({ id: user.id, firstName: user.firstName, lastName: user.lastName})
    currentPost.likedByAuthenticatedUser = true;
  }

  getLikedByUser(): void {
    if (!this.isAuthenticated) {
      return;
    }
    const userId = this.userService.getUser().id;
    for (let post of this.posts) {
      this.likeService
        .getLikesByUserAndPost(post.id, userId)
        .subscribe((liked) => {
          post.likedByAuthenticatedUser = liked;
        });
    }
  }

  getLikes(): void {
    for (let post of this.posts) {
      this.likeService.getLikesByPost(post.id).subscribe((likes) => {
        post.likes = likes;
      });
    }
  }

  getComments(): void {
    for (let post of this.posts) {
      this.commentService.getCommentsByPost(post.id).subscribe((comments) => {
        post.comments = comments;
      });
    }
  }

  openDeleteConfirmationPopUp(postId: number, postTitle: string) {
    const deleteDialog = this.dialog.open(PostDeleteDialogComponent, {
      data: { title: postTitle },
    });

    deleteDialog.afterClosed().subscribe((result) => {
      if (!result) return;
      this.postService.delete(postId).subscribe({
        next: () => {
          this.fetchData();
        },
        error: (error) => {
          console.error(error);
          this.fetchData();
        },
      });
    });
  }

  setPermissions(): void {
    // Set permissions for admin user
    const adminUser = this.userService.getUser().isAdmin;
    if (adminUser) {
      this.posts.map((post) => (post.canEdit = true));
      return;
    }
    // Set permissions for unauthenticated user
    if (!this.isAuthenticated) {
      this.posts.map((post) => this.setPermissionsForUnauthenticatedUser(post));
      return;
    }
    // Set permissions for bloggers Users
    const teamUserId = this.userService.getUser().teamId;
    const userId = this.userService.getUser().id;
    for (let post of this.posts) {
      const isSameTeam = post.user.team.id === teamUserId;
      const isOwner = post.user.id === userId;
      // Set permissions for authenticated user
      this.setPermissionsForAuthenticatedUser(post, isSameTeam, isOwner);
    }
  }

  private setPermissionsForUnauthenticatedUser(post: Post): void {
    const publicAccess = post.category_permission.some(
      (cp) =>
        cp.category === Category.PUBLIC && cp.permission === Permission.EDIT
    );
    if (publicAccess) post.canEdit = true;
  }

  private setPermissionsForAuthenticatedUser(
    post: Post,
    isSameTeam: boolean,
    isOwner: boolean
  ): void {

    if (isOwner) {
      post.canEdit = this.hasPermission(post, Category.AUTHOR, Permission.EDIT);
      return;
    }
    if (isSameTeam) {
      post.canEdit = this.hasPermission(post, Category.TEAM, Permission.EDIT);
      return;
    }
    const publicAccess = this.hasPermission(post, Category.PUBLIC, Permission.EDIT);
    const authenticatedAccess = this.hasPermission(post, Category.AUTHENTICATED, Permission.EDIT);
    post.canEdit = publicAccess || authenticatedAccess;
  }

  private hasPermission(
    post: Post,
    category: Category,
    permission: Permission
  ): boolean {
    const hasPermission = post.category_permission.some(
      (cp) => cp.category === category && cp.permission === permission
    );
    return hasPermission;
  }
}
