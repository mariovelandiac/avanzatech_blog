import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommentActionComponent } from './comment-action.component';
import { RouterTestingModule } from '@angular/router/testing';

describe('CommentActionComponent', () => {
  let component: CommentActionComponent;
  let fixture: ComponentFixture<CommentActionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CommentActionComponent, RouterTestingModule.withRoutes([])]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CommentActionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
