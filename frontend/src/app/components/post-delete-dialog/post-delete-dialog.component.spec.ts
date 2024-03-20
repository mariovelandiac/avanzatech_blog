import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostDeleteDialogComponent } from './post-delete-dialog.component';
import { MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { mockPost } from '../../test-utils/post.model.mock';

describe('PostDeleteDialogComponent', () => {
  let component: PostDeleteDialogComponent;
  let fixture: ComponentFixture<PostDeleteDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatDialogModule],
      providers: [
        {
          provide: MAT_DIALOG_DATA,
          useValue: { title: mockPost.title }
        }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostDeleteDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
