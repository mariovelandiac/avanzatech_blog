import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CommentCounterComponent } from './comment-counter.component';
import { RouterTestingModule } from '@angular/router/testing';
import { mockCommentListDTO } from '../../test-utils/comment.model.mock';
import { Router } from '@angular/router';

describe('CommentCounterComponent', () => {
  let component: CommentCounterComponent;
  let fixture: ComponentFixture<CommentCounterComponent>;
  let router: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CommentCounterComponent, RouterTestingModule.withRoutes([])]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CommentCounterComponent);
    component = fixture.componentInstance;
    component.comments = mockCommentListDTO;
    component.postId = mockCommentListDTO.results[0].post;
    router = TestBed.inject(Router);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render comment counter', () => {
    // Arrange
    const elements = fixture.nativeElement.querySelectorAll('.like-comment-home-item p');
    const counter = elements[0];
    const expectedText = `${component.commentCounter} Comment${component.commentPlural}`;
    // Assert
    expect(counter.innerText).toContain(expectedText);
  });

  it('should render comment in singular form if there is only one comment', () => {
    // Arrange
    const commentDTO = mockCommentListDTO;
    // There is only two comments
    commentDTO.results.pop();
    // Act
    fixture.detectChanges();
    const elements = fixture.nativeElement.querySelectorAll('.like-comment-home-item p');
    const counter = elements[0];
    const expectedText = `${component.commentCounter} Comment`;
    // Assert
    expect(counter.innerText).toContain(expectedText);
  });

  it('should render comment in plural form if there is more than one comment', () => {
    // Arrange
    const commentDTO = mockCommentListDTO;
    // There is only one comment
    commentDTO.results.push(commentDTO.results[0]);
    // Act
    fixture.detectChanges();
    const elements = fixture.nativeElement.querySelectorAll('.like-comment-home-item p');
    const counter = elements[0];
    const expectedText = `${component.commentCounter} Comment${component.commentPlural}`;
    // Assert
    expect(counter.innerText).toContain(expectedText);
  });

  it('should show loading message if comments are not loaded', () => {
    // Arrange
    component.comments = undefined;
    // Act
    fixture.detectChanges();
    const elements = fixture.nativeElement.querySelectorAll('.like-comment-home-item p');
    const counter = elements[0];
    const expectedText = 'Loading...';
    // Assert
    expect(counter.innerText).toContain(expectedText);
  });

  it('should redirect to post detail page on click', () => {
    // Arrange
    const elements = fixture.nativeElement.querySelectorAll('.like-comment-home-item p');
    const element = elements[0];
    const expectedRoute = `/post/${component.postId}`;
    const navigateByUrlSpy = spyOn(router, 'navigateByUrl') as jasmine.Spy;
    // Act
    element.click();
    // Assert
    const navArgs = navigateByUrlSpy.calls.first().args[0];
    expect(router.navigateByUrl).toHaveBeenCalled();
    expect(expectedRoute).toContain(navArgs);
  });
});
