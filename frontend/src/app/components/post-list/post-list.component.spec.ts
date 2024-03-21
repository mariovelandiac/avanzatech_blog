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
import { throwError } from 'rxjs';
import { Permission } from '../../models/enums/permission.enum';

describe('PostListComponent', () => {
  let component: PostListComponent;
  let postService: PostService;
  let likeService: LikeService;
  let commentService: CommentService;
  let authService: AuthService;
  let userService: UserStateService;
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
    authService = TestBed.inject(AuthService);
    userService = TestBed.inject(UserStateService);
    fixture.detectChanges();
  });

  afterEach(() => {
    const user = userService.getUser();
    user.isAdmin = false;
    component.posts.every(post => post.canEdit = false);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set authentication status on init', () => {
    // Arrange
    authService.setAuthentication(true);
    // Act & Assert
    expect(component.isAuthenticated).toBeTrue();
    // Arrange
    authService.setAuthentication(false);
    // Act & Assert
    expect(component.isAuthenticated).toBeFalse();
  });

  it('should fetch data on init', () => {
    // Arrange
    const spy = spyOn(postService, 'list').and.callThrough();
    // Act
    component.ngOnInit();
    // Assert
    expect(spy).toHaveBeenCalled();
  });

  it('should set posts and count on successful fetch', () => {
    // Arrange
    const pageIndex = 1; // Example page index
    const errorMessage = 'An unexpected error has occurred';

    // Temporarily change the behavior of the list method to throw an error
    const spy = spyOn(mockPostService.prototype, 'list').and.returnValue(throwError(() => new Error(errorMessage)));

    // Act
    component.fetchData(pageIndex);

    // Assert
    expect(component.wasAnError).toBeTrue();
    expect(component.errorMessage.toString()).toContain(errorMessage);
  });

  it('should reset error status on destroy', () => {
    // Arrange
    component.wasAnError = true;
    component.errorMessage = 'An unexpected error has occurred';
    // Act
    component.ngOnDestroy();
    // Assert
    expect(component.wasAnError).toBeFalse();
    expect(component.errorMessage).toBe('');
  });

  describe('Like handlers', () => {
    it('should handle like action when a like is being added', () => {
      // Arrange
      const spy = spyOn(likeService, 'createLike').and.callThrough();
      const isLiked = false;
      // Act
      component.handleLikeAction(isLiked, 1);
      // Assert
      expect(spy).toHaveBeenCalled();
    });

    it('should handle like action when a like is being removed', () => {
      // Arrange
      const spy = spyOn(likeService, 'deleteLike').and.callThrough();
      const isLiked = true;
      // Act
      component.handleLikeAction(isLiked, 1);
      // Assert
      expect(spy).toHaveBeenCalled();
    });

    it('should update reference to post when a like is being added', () => {
      // Arrange
      const isLiked = false;
      const post = component.posts[0];
      // Act
      component.handleLikeAction(isLiked, component.posts[0].id);
      // Assert
      expect(post).not.toBe(component.posts[0]);
    });

    it('should increase like count and add user to likedBy when a like is being added', () => {
      // Arrange
      const isLiked = false;
      const post = component.posts[0];
      const previousLikesCount = post.likes!.count;
      // Act
      component.handleLikeAction(isLiked, component.posts[0].id);
      // Assert
      expect(component.posts[0].likes!.count).toBe(previousLikesCount + 1);
      expect(component.posts[0].likedByAuthenticatedUser).toBeTrue();
    });

    it('should decrease like count and remove user from likedBy when a like is being removed', () => {
      // Arrange
      const isLiked = true;
      const post = component.posts[0];
      const previousLikesCount = post.likes!.count;
      // Act
      component.handleLikeAction(isLiked, component.posts[0].id);
      // Assert
      expect(component.posts[0].likes!.count).toBe(previousLikesCount - 1);
      expect(component.posts[0].likedByAuthenticatedUser).toBeFalse();
    });

    it('should call getLikesByPost when a like page is being changed', () => {
      // Arrange
      const spy = spyOn(component, 'getLikesByPost').and.callThrough();
      const pageIndex = 1;
      // Act
      component.handleLikePageChange(pageIndex, component.posts[0]);
      // Assert
      expect(spy).toHaveBeenCalled();
    });

    it('should not get liked by user when user is not authenticated', () => {
      // Arrange
      authService.setAuthentication(false);
      const spy = spyOn(likeService, 'getLikeByUserAndPost').and.callThrough();
      // Act
      component.getLikedByUser();
      // Assert
      expect(spy).not.toHaveBeenCalled();
    });

    it('should get liked by user when user is authenticated', () => {
      // Arrange
      authService.setAuthentication(true);
      const spy = spyOn(likeService, 'getLikeByUserAndPost').and.callThrough();
      // Act
      component.getLikedByUser();
      // Assert
      expect(spy).toHaveBeenCalled();
      expect(component.posts[0].likedByAuthenticatedUser).toBeDefined();
    });

    it('should get likes by post', () => {
      // Arrange
      const spy = spyOn(likeService, 'getLikesByPost').and.callThrough();
      // Act
      component.getLikesByPost(component.posts[0]);
      // Assert
      expect(spy).toHaveBeenCalled();
      expect(component.posts[0].likes).toBeDefined();
    });
  })

  describe('Comment handlers', () => {
    it('should get comments', () => {
      // Arrange
      const spy = spyOn(commentService, 'getCommentsByPost').and.callThrough();
      // Act
      component.getComments();
      // Assert
      expect(spy).toHaveBeenCalled();
      expect(component.posts[0].comments).toBeDefined();
    });
  });

  it('should set permissions', () => {
    // Arrange
    const user = userService.getUser();
    user.isAdmin = true;
    // Act
    component.setPermissions();
    // Assert
    expect(component.posts.every(post => post.canEdit)).toBeTrue();
  });

  it('should set permissions for unauthenticated user', () => {
    // Arrange
    component.isAuthenticated = false;
    // Act
    component.setPermissions();
    // Assert
    component.posts.forEach(post => {
      expect(post.canEdit).toBeFalse();
    });
  });

  it('should set can edit as true if user has permission', () => {
    // Arrange
    const user = userService.getUser();
    user.isAdmin = false;
    authService.setAuthentication(true);
    const postEdit = component.posts[0];
    postEdit.category_permission[3].permission = Permission.EDIT;
    console.log(postEdit)
    // Act
    component.setPermissions();
    // Assert
    expect(component.posts.find(post => post.id == postEdit.id)?.canEdit).toBeTrue();
    // Revert changes
    component.posts[0].category_permission[3].permission = Permission.READ;
  });

});
