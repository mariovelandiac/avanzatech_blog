import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LikeActionComponent } from './like-action.component';

describe('LikeActionComponent', () => {
  let component: LikeActionComponent;
  let fixture: ComponentFixture<LikeActionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LikeActionComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(LikeActionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
