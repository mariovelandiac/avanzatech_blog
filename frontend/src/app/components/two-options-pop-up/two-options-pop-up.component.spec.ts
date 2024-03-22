import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TwoOptionsPopUpComponent } from './two-options-pop-up.component';

describe('TwoOptionsPopUpComponent', () => {
  let component: TwoOptionsPopUpComponent;
  let fixture: ComponentFixture<TwoOptionsPopUpComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TwoOptionsPopUpComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TwoOptionsPopUpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
