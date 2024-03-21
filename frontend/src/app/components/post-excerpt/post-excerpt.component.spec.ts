import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { PostExcerptComponent } from './post-excerpt.component';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { mockPost } from '../../test-utils/post.model.mock';

describe('PostContentComponent', () => {
  let component: PostExcerptComponent;
  let fixture: ComponentFixture<PostExcerptComponent>;
  let router: Router;

  beforeEach(waitForAsync(() => {

    TestBed.configureTestingModule({
      imports: [RouterTestingModule.withRoutes([])]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostExcerptComponent);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    component.postId = mockPost.id;
    component.excerpt = mockPost.excerpt;
    fixture.detectChanges();
  }));

  it('should create', () => {
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });

  it('should render post excerpt', () => {
    const excerpt = fixture.nativeElement.querySelector('.post-content');
    expect(excerpt.textContent).toContain(mockPost.excerpt+"...");
  });

  it('should display show more link if excerpt is longer than 200 characters', () => {
    // Arrange
    component.excerpt = 'a'.repeat(201);
    // Act
    fixture.detectChanges();
    const showMore = fixture.nativeElement.querySelector('.post-content a');
    // Assert
    expect(showMore).toBeTruthy();
    expect(showMore.textContent).toContain('Show more');
    expect(showMore.getAttribute('href')).toContain(`/post/${component.postId}`);
    // Revert changes
    component.excerpt = 'Test Post Excerpt';
  });

  it('should not display show more link if excerpt is shorter than 200 characters', () => {
    // Arrange
    component.excerpt = 'a'.repeat(199);
    // Act
    fixture.detectChanges();
    const showMore = fixture.nativeElement.querySelector('.post-content a');
    // Assert
    expect(showMore).toBeFalsy();
    // Revert changes
    component.excerpt = 'Test Post Excerpt';
  });
});
