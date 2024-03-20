import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostListComponent } from './post-list.component';
import { PostService } from '../../services/post.service';
import { mockPostService } from '../../test-utils/post.service.mock';
import { RouterTestingModule } from '@angular/router/testing';
import { LikeService } from '../../services/like.service';
import { mockLikeService } from '../../test-utils/like.service.mock';
import { CommentService } from '../../services/comment.service';
import { mockCommentService } from '../../test-utils/comment.service.mock';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { AuthService } from '../../services/auth.service';
import { MockAuthService } from '../../test-utils/auth.mock';
import { UserStateService } from '../../services/user-state.service';
import { mockUserStateService } from '../../test-utils/user.service.mock';

describe('PostListComponent', () => {
  let component: PostListComponent;
  let postService: PostService;
  let likeService: LikeService;
  let commentService: CommentService
  let authService: AuthService;
  let fixture: ComponentFixture<PostListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule.withRoutes([]), HttpClientTestingModule],
      providers: [
        {
          provide: PostService,
          useClass: mockPostService
        },
        {
          provide: LikeService,
          useClass: mockLikeService
        },
        {
          provide: CommentService,
          useClass: mockCommentService
        },
        {
          provide: AuthService,
          useClass: MockAuthService
        },
        {
          provide: UserStateService,
          useClass: mockUserStateService
        }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostListComponent);
    component = fixture.componentInstance;
    postService = TestBed.inject(PostService);
    likeService = TestBed.inject(LikeService);
    commentService = TestBed.inject(CommentService);
    authService = TestBed.inject(AuthService)
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
