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

@Component({
  selector: 'app-post-list',
  standalone: true,
  imports: [PostContentComponent, LikeCounterComponent, CommentCounterComponent,LikeActionComponent, CommentActionComponent, EditActionComponent, DeleteActionComponent,CommonModule],
  templateUrl: './post-list.component.html',
  styleUrl: './post-list.component.sass'
})
export class PostListComponent implements OnInit {
  posts!: Post[];
  isAuthenticated = false;

  constructor(
    private postService: PostService,
    private likeService: LikeService,
    private commentService: CommentService,
    private authService: AuthService,
    private userService: UserStateService
  ) {}


  ngOnInit() {
    this.authService.isAuthenticated$.subscribe(isAuthenticated => {
      this.isAuthenticated = isAuthenticated;
    });
    this.postService.list().subscribe(posts => {
      this.posts = posts;
      this.getLikedByUser();
      // To do: set permissions
      this.setPermissions();
      this.getLikes();
      this.getComments();
    });
  }

  handleLikeAction(isLiked: boolean, postId: number): void {
    const currentPostIndex = this.posts.findIndex(post => post.id === postId);
    isLiked ? this.handleDeleteLike(currentPostIndex) : this.handleCreateLike(currentPostIndex);
  }

  handleDeleteLike(currentPostIndex: number): void {
    const currentPost = this.posts[currentPostIndex];
    const userId = this.userService.getUser().id;
    this.likeService.deleteLike(currentPost.id, userId).subscribe(() => {});
    currentPost.likes!.count--;
    currentPost.likedByAuthenticatedUser = false;
    this.posts[currentPostIndex] = { ...currentPost };
  }

  handleCreateLike(currentPostIndex: number): void {
    const currentPost = this.posts[currentPostIndex];
    const userId = this.userService.getUser().id;
    this.likeService.createLike(currentPost.id, userId).subscribe(() => {});
    currentPost.likes!.count++;
    currentPost.likedByAuthenticatedUser = true;
    this.posts[currentPostIndex] = { ...currentPost };
  }

  getLikedByUser(): void {
    if (!this.isAuthenticated) {
      return;
    }
    const userId = this.userService.getUser().id;
    for (let post of this.posts) {
      this.likeService.getLikesByUserAndPost(post.id, userId).subscribe(liked => {
        post.likedByAuthenticatedUser = liked;
      });
    }
  }

  setPermissions(): void {
    // for (let post of this.posts) {
    //   console.log(post.category_permission);
    //   console.log(this.userService.getUser().teamId);
    // }
  }

  getLikes(): void {
    for (let post of this.posts) {
      this.likeService.getLikesByPost(post.id).subscribe(likes => {
        post.likes = likes;
      });
    }
  }

  getComments(): void {
    for (let post of this.posts) {
      this.commentService.getCommentsByPost(post.id).subscribe(comments => {
        post.comments = comments;
      });
    }
  }

}
