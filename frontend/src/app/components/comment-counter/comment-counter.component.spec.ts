import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommentCounterComponent } from './comment-counter.component';
import { RouterTestingModule } from '@angular/router/testing';

describe('CommentCounterComponent', () => {
  let component: CommentCounterComponent;
  let fixture: ComponentFixture<CommentCounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CommentCounterComponent, RouterTestingModule.withRoutes([])]
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
