import { Component, OnInit } from '@angular/core';
import { PostContentComponent } from '../post-content/post-content.component';
import { Post } from '../../models/interfaces/post.interface';
import { PostService } from '../../services/post.service';
import { CommonModule } from '@angular/common';
import { LikeCounterComponent } from '../like-counter/like-counter.component';
import { CommentCounterComponent } from '../comment-counter/comment-counter.component';
import { InteractionBarComponent } from '../interaction-bar/interaction-bar.component';
import { LikeService } from '../../services/like.service';
import { CommentService } from '../../services/comment.service';
import { AuthService } from '../../services/auth.service';
import { UserStateService } from '../../services/user-state.service';

@Component({
  selector: 'app-post-list',
  standalone: true,
  imports: [PostContentComponent, LikeCounterComponent, CommentCounterComponent,InteractionBarComponent, CommonModule],
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
  ) {}

  ngOnInit() {
    this.postService.list().subscribe(posts => {
      this.posts = posts;
      this.getLikes();
      this.getComments();
    });
    this.authService.isAuthenticated$.subscribe(isAuthenticated => {
      this.isAuthenticated = isAuthenticated;
    });
  }

  getLikes() {
    for (let post of this.posts) {
      this.likeService.getLikesByPost(post.id).subscribe(likes => {
        post.likes = likes;
      });
    }
  }

  getComments() {
    for (let post of this.posts) {
      this.commentService.getCommentsByPost(post.id).subscribe(comments => {
        post.comments = comments;
      });
    }
  }
}
