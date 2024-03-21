import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LikeCounterComponent } from './like-counter.component';
import { mockLikeList } from '../../test-utils/like.model.mock';
import { COMPILER_OPTIONS } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';

describe('LikeCounterComponent', () => {
  let component: LikeCounterComponent;
  let fixture: ComponentFixture<LikeCounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LikeCounterComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LikeCounterComponent);
    component = fixture.componentInstance;
    component.likes = mockLikeList;
    component.ngOnChanges();
    fixture.detectChanges();
  });

  describe('Render component', () => {
    it('should create', () => {
      expect(component).toBeTruthy();
    });

    it('should show the number of likes', () => {
      // Arrange
      const likeCounter = fixture.nativeElement.querySelector('.like-counter');
      // Act & Assert
      expect(likeCounter.textContent).toContain(component.likeCounter);
    });

    it('should show singular like without the "s"', () => {
      // Arrange
      const likes = {...mockLikeList};
      likes.count = 1;
      likes.likedBy = [mockLikeList.likedBy[0]];
      component.likes = likes;
      // Act
      component.ngOnChanges();
      fixture.detectChanges();
      const likeCounter = fixture.nativeElement.querySelector('.like-counter');
      // Assert
      expect(likeCounter.textContent).toContain('1 Like');
    });

    it('should show the likes in plural if there are more than 1', () => {
      // Arrange
      const likes = {...mockLikeList};
      likes.count = 2;
      likes.likedBy = [mockLikeList.likedBy[0], mockLikeList.likedBy[1]];
      component.likes = likes;
      // Act
      component.ngOnChanges();
      fixture.detectChanges();
      const likeCounter = fixture.nativeElement.querySelector('.like-counter');
      // Assert
      expect(likeCounter.textContent).toContain('2 Likes');
    });

    it('should set likeCounter when likes are set', () => {
      // Arrange
      const likes = {...mockLikeList};
      likes.count = 2;
      likes.likedBy = [mockLikeList.likedBy[0], mockLikeList.likedBy[1]];
      // Act
      component.likes = likes;
      component.ngOnChanges();
      // Assert
      expect(component.likeCounter).toBe(2);
    });

    it('should set the mouse pointer to pointer if there are likes', () => {
      // Arrange
      const likes = {...mockLikeList};
      likes.count = 2;
      likes.likedBy = [mockLikeList.likedBy[0], mockLikeList.likedBy[1]];
      // Act
      component.likes = likes;
      component.ngOnChanges();
      fixture.detectChanges();
      const likeCounter = fixture.nativeElement.querySelector('.like-counter');
      // Assert
      expect(likeCounter.style.cursor).toBe('pointer');
    });

    it('should set the mouse pointer to default if there are no likes', () => {
      // Arrange
      const likes = {
        count: 0,
        likedBy: [],
      };
      // Act
      component.likes = likes;
      component.ngOnChanges();
      fixture.detectChanges();
      const likeCounter = fixture.nativeElement.querySelector('.like-counter');
      // Assert
      expect(likeCounter.style.cursor).toBe('default');
    });

    it('should show "Loading" when there are no likes', () => {
      // Arrange
      component.likes = undefined;
      // Act
      fixture.detectChanges();
      const elements = fixture.nativeElement.querySelectorAll('.like-comment-home-item p');
      const loading = elements[0];
      // Assert
      expect(loading.innerText).toContain('Loading');
    });

    it('should show the likedBy when the user clicks on the like counter', () => {
      // Arrange
      const likeCounter = fixture.nativeElement.querySelector('.like-counter');
      // Act
      likeCounter.click();
      fixture.detectChanges();
      const likedBy = fixture.nativeElement.querySelector('.floating-message');
      // Assert
      expect(likedBy).toBeTruthy();
    });

    it('should show pageSize likes per page at most', () => {
      // Arrange
      component.likes = mockLikeList;
      component.ngOnChanges();
      const likeCounter = fixture.nativeElement.querySelector('.like-counter');
      // Act
      likeCounter.click();
      fixture.detectChanges();
      // Assert
      expect(component.likedBy.length).toBeLessThanOrEqual(component.pageSize);
    });

    it('should should show pageSize pages at most per page when a new like is added', () => {
      // Arrange
      const likes = {...mockLikeList};
      likes.count = 16;
      const likeCounter = fixture.nativeElement.querySelector('.like-counter');
      // Act
      component.likes = likes;
      component.ngOnChanges();
      likeCounter.click();
      fixture.detectChanges();
      // Assert
      expect(component.likedBy.length).toBeLessThanOrEqual(component.pageSize);
    });

    it('should show pageSize - 1 likes if there was pageSize likes and the user removes one', () => {
      // Arrange
      const likes = {...mockLikeList};
      likes.count = 14;
      likes.likedBy = likes.likedBy.slice(1);
      const likeCounter = fixture.nativeElement.querySelector('.like-counter');
      // Act
      component.likes = likes;
      component.ngOnChanges();
      likeCounter.click();
      fixture.detectChanges();
      // Assert
      expect(component.likedBy.length).toEqual(component.pageSize - 1);
    });

    it('should not show paginator if likes.likedBy.length is equal or less than pageSize', () => {
      // Arrange
      const likes = {...mockLikeList};
      likes.count = 10;
      const likeCounter = fixture.nativeElement.querySelector('.like-counter');
      // Act
      component.likes = likes;
      component.ngOnChanges();
      likeCounter.click();
      fixture.detectChanges();
      const paginator = fixture.nativeElement.querySelector('.mat-paginator');
      // Assert
      expect(paginator).toBeFalsy();
    });
  });

  describe('Page change', () => {
    it('should emit the page change event', () => {
      // Arrange
      const likeCounter = fixture.nativeElement.querySelector('.like-counter');
      const spy = spyOn(component.pageChange, 'emit');
      // Act
      likeCounter.click();
      fixture.detectChanges();
      component.handlePageChange({pageIndex: 1} as PageEvent);
      // Assert
      expect(spy).toHaveBeenCalled();
    });
  });
});
