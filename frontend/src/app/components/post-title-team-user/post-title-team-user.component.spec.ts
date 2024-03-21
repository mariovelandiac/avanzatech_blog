import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostTitleTeamUserComponent } from './post-title-team-user.component';
import { mockCreatedAt, mockPost } from '../../test-utils/post.model.mock';
import { Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';

describe('PostTitleTeamUserComponent', () => {
  let component: PostTitleTeamUserComponent;
  let fixture: ComponentFixture<PostTitleTeamUserComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule.withRoutes([])],
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostTitleTeamUserComponent);
    component = fixture.componentInstance;
    component.post = mockPost;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render post title', () => {
    const title = fixture.nativeElement.querySelector('.phtitle-h1');
    expect(title.textContent).toContain(mockPost.title);
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


});
