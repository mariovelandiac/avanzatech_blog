import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LikeCounterComponent } from './like-counter.component';

describe('LikeCounterComponent', () => {
  let component: LikeCounterComponent;
  let fixture: ComponentFixture<LikeCounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LikeCounterComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(LikeCounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
