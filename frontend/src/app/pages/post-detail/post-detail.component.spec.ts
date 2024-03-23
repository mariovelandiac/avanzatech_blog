import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostDetailComponent } from './post-detail.component';
import { PostService } from '../../services/post.service';
import { mockPostService } from '../../test-utils/post.service.mock';
import { LikeService } from '../../services/like.service';
import { mockLikeService } from '../../test-utils/like.service.mock';
import { CommentService } from '../../services/comment.service';
import { mockCommentService } from '../../test-utils/comment.service.mock';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingHarness, RouterTestingModule } from '@angular/router/testing';

describe('PostDetailComponent', () => {
  let component: PostDetailComponent;
  let fixture: ComponentFixture<PostDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, RouterTestingModule.withRoutes([])],
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
        }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
