import { Component, OnInit } from '@angular/core';
import { PostTitleTeamUserComponent } from '../../components/post-title-team-user/post-title-team-user.component';
import { PostService } from '../../services/post.service';
import { LikeService } from '../../services/like.service';
import { CommentService } from '../../services/comment.service';
import { AuthService } from '../../services/auth.service';
import { ActivatedRoute, Router } from '@angular/router';
import { PostRetrieve } from '../../models/interfaces/post.interface';
import { CommonModule, DatePipe } from '@angular/common';
import { Title } from '@angular/platform-browser';
import { LikeCounterComponent } from '../../components/like-counter/like-counter.component';
import { LikeList } from '../../models/interfaces/like.interface';
import { CommentList, CommentCreated } from '../../models/interfaces/comment.interface';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { Pagination } from '../../models/enums/constants.enum';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { UnexpectedErrorComponent } from '../../components/unexpected-error/unexpected-error.component';
import { UserStateService } from '../../services/user-state.service';
import { User } from '../../models/interfaces/user.interface';
import { BackButtonComponent } from '../../components/back-button/back-button.component';

@Component({
  selector: 'app-post-detail',
  standalone: true,
  imports: [
    PostTitleTeamUserComponent,
    LikeCounterComponent,
    MatPaginatorModule,
    CommonModule,
    DatePipe,
    ReactiveFormsModule,
    UnexpectedErrorComponent,
    BackButtonComponent
  ],
  templateUrl: './post-detail.component.html',
  styleUrl: './post-detail.component.sass'
})
export class PostDetailComponent implements OnInit {
  isAuthenticated = false;
  pageTitle = 'Post Detail';
  postId!: number;
  post: PostRetrieve | undefined;
  likes: LikeList | undefined;
  comments: CommentList | undefined;
  commentCount: number = 0;
  previousComments: CommentList | undefined;
  previousCommentPageIndex = 0;
  commentPageSize = Pagination.COMMENT_PAGE_SIZE;
  commentForm!: FormGroup;
  wasAnError = false;
  errorMessage: string = '';

  constructor(
    private postService: PostService,
    private likeService: LikeService,
    private commentService: CommentService,
    private authService: AuthService,
    private userService: UserStateService,
    private route: ActivatedRoute,
    private router: Router,
    private title: Title,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.title.setTitle(this.pageTitle);
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isAuthenticated = isAuthenticated;
      if (!isAuthenticated) return;
      this.commentForm = this.formBuilder.group({
        content: ['', [Validators.required]],
      });
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
        this.wasAnError = true;
        this.errorMessage = error.message;
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

  getCommentsByPost(pageIndexComments: number = 0): void {
    this.commentService.getCommentsByPost(this.postId, pageIndexComments).subscribe((comments) => {
      this.comments = comments;
      this.commentCount = comments.count;
    });
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


  onSubmit() {
    if (this.commentForm.invalid || !this.isAuthenticated) return;
    const content = this.commentForm.value.content;
    const user = this.userService.getUser();
    this.commentService.createComment(this.postId, user.id, content).subscribe((comment) => {
      this.addCommentToLayout(comment, user);
      this.commentCount++;
      this.commentForm.reset();
    });
  }

  addCommentToLayout(comment: CommentCreated, user: User) {
    // If pagination is applied, the comment will be added to the next page, and fetched by page event
    if (this.comments!.results.length == this.commentPageSize) return;
    const layOutComment = {
      user: {
        firstName: user.firstName,
        lastName: user.lastName
      },
      content: comment.content,
      createdAt: comment.createdAt,
      id: comment.id
    }
    this.comments!.results.push(layOutComment);
  }

  onCancel() {
    this.commentForm.reset();
  }

  goBack() {
    this.router.navigate(['/home']);
  }

  get commentsBy() {
    return this.comments?.results;
  }

  get content() {
    return this.post?.content;
  }

}
