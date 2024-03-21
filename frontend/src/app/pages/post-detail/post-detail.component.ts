import { Component, OnInit } from '@angular/core';
import { PostTitleTeamUserComponent } from '../../components/post-title-team-user/post-title-team-user.component';
import { PostService } from '../../services/post.service';
import { LikeService } from '../../services/like.service';
import { CommentService } from '../../services/comment.service';
import { AuthService } from '../../services/auth.service';
import { ActivatedRoute } from '@angular/router';
import { PostRetrieve } from '../../models/interfaces/post.interface';
import { CommonModule, DatePipe } from '@angular/common';
import { Title } from '@angular/platform-browser';
import { LikeCounterComponent } from '../../components/like-counter/like-counter.component';
import { LikeList } from '../../models/interfaces/like.interface';
import { CommentList, CommentListDTO } from '../../models/interfaces/comment.interface';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { Pagination } from '../../models/enums/constants.enum';

@Component({
  selector: 'app-post-detail',
  standalone: true,
  imports: [
    PostTitleTeamUserComponent,
    LikeCounterComponent,
    MatPaginatorModule,
    CommonModule,
    DatePipe,
  ],
  templateUrl: './post-detail.component.html',
  styleUrl: './post-detail.component.sass'
})
export class PostDetailComponent implements OnInit {
  isAuthenticated = false;
  postId!: number;
  post: PostRetrieve | undefined;
  likes: LikeList | undefined;
  comments: CommentList | undefined;
  previousComments: CommentList | undefined;
  previousCommentPageIndex = 0;
  commentPageSize = Pagination.COMMENT_PAGE_SIZE;
  pageTitle = 'Post Detail';

  constructor(
    private postService: PostService,
    private likeService: LikeService,
    private commentService: CommentService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private title: Title
  ) {}

  ngOnInit(): void {
    this.title.setTitle(this.pageTitle);
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isAuthenticated = isAuthenticated;
    });
    this.route.paramMap.subscribe((params) => {
      this.postId = +params.get('id')!;
      this.fetchData();
    });
  };

  fetchData() {
    this.postService.retrieve(this.postId).subscribe({
      next: (post) => {
        this.post = post;
        this.title.setTitle(this.pageTitle + ' - ' + this.post?.title);
        this.getLikesByPost();
        this.getCommentsByPost();
      },
      error: (error) => {
        console.error(error);
      }
    });
  }

  getLikesByPost(pageIndexLikes: number = 0): void {
    this.likeService.getLikesByPost(this.postId, pageIndexLikes).subscribe((likes) => {
      this.likes = likes;
    });
  }

  handleLikePageChange(pageIndexLikes: number): void {
    this.getLikesByPost(pageIndexLikes);
  }

  handleCommentPageChange(e: PageEvent): void {
    const currentPageIndex = e.pageIndex;
    const moveForward = currentPageIndex > this.previousCommentPageIndex;
    this.previousCommentPageIndex = currentPageIndex;
    // Move forward
    if (!this.previousComments || moveForward) {
      this.previousComments = this.comments;
      this.getCommentsByPost(currentPageIndex);
    } else {
      // If the user is moving backwards, use the previousComments
      this.comments = this.previousComments;
      this.previousComments = undefined;
    }
  }

  getCommentsByPost(pageIndexComments: number = 0): void {
    this.commentService.getCommentsByPost(this.postId, pageIndexComments).subscribe((comments) => {
      this.comments = comments;
    });
  }

  get commentsBy() {
    return this.comments?.results;
  }

  get content() {
    return this.post?.content;
  }

  get commentCount() {
    return this.comments!.count;
  }
}
