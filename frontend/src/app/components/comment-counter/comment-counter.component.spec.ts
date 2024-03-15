import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommentCounterComponent } from './comment-counter.component';

describe('CommentCounterComponent', () => {
  let component: CommentCounterComponent;
  let fixture: ComponentFixture<CommentCounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CommentCounterComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CommentCounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
