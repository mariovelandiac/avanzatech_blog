import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommentActionComponent } from './comment-action.component';

describe('CommentActionComponent', () => {
  let component: CommentActionComponent;
  let fixture: ComponentFixture<CommentActionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CommentActionComponent]
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
