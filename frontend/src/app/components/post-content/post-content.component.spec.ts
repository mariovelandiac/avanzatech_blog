import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { PostContentComponent } from './post-content.component';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { Post } from '../../models/interfaces/post.interface';
import { mockPost } from '../../test-utils/post.model.mock';

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
    console.log("hellloooo");
    expect(component).toBeTruthy();
  });
});
