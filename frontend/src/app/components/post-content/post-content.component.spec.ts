import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { PostContentComponent } from './post-content.component';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { Post } from '../../models/interfaces/post.interface';
import { mockCreatedAt, mockPost } from '../../test-utils/post.model.mock';

describe('PostContentComponent', () => {
  let component: PostContentComponent;
  let fixture: ComponentFixture<PostContentComponent>;
  let router: Router;

  beforeEach(waitForAsync(() => {

    TestBed.configureTestingModule({
      imports: [RouterTestingModule.withRoutes([])]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostContentComponent);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    component.post = mockPost;
    fixture.detectChanges();
  }));

  it('should create', () => {
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });

  it('should render post title', () => {
    const title = fixture.nativeElement.querySelector('.phtitle-h1');
    expect(title.textContent).toContain(mockPost.title);
  });

  it('should render post excerpt', () => {
    const excerpt = fixture.nativeElement.querySelector('.post-content');
    expect(excerpt.textContent).toContain(mockPost.excerpt+"...");
  });

  it('should render user team', () => {
    const elements = fixture.nativeElement.querySelectorAll('.user-team-container li');
    const team = elements[0].innerText;
    expect(team).toContain(mockPost.user.team.name);
  });

  it('should render user name', () => {
    const elements = fixture.nativeElement.querySelectorAll('.user-team-container li');
    const user = elements[1].innerText;
    expect(user).toContain(`${mockPost.user.firstName} ${mockPost.user.lastName}`);
  });

  it('should render post created at', () => {
    // Arrange
    const expectedDate = mockCreatedAt;
    const elements = fixture.nativeElement.querySelectorAll('.user-team-container li');
    const createdAt = elements[2].innerText;
    // Assert
    expect(createdAt).toEqual(expectedDate);
  })

  it('should display show more link if excerpt is longer than 200 characters', () => {
    // Arrange
    component.post!.excerpt = 'a'.repeat(201);
    // Act
    fixture.detectChanges();
    const showMore = fixture.nativeElement.querySelector('.post-content a');
    // Assert
    expect(showMore).toBeTruthy();
    expect(showMore.textContent).toContain('Show more');
    expect(showMore.getAttribute('href')).toContain(`/post/${component.id}`);
  });

  it('should not display show more link if excerpt is shorter than 200 characters', () => {
    // Arrange
    component.post!.excerpt = 'a'.repeat(199);
    // Act
    fixture.detectChanges();
    const showMore = fixture.nativeElement.querySelector('.post-content a');
    // Assert
    expect(showMore).toBeFalsy();
  });
});
