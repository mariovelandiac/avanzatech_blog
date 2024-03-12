import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RequiredFieldComponent } from './required-field.component';

describe('RequiredFieldComponent', () => {
  let component: RequiredFieldComponent;
  let fixture: ComponentFixture<RequiredFieldComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RequiredFieldComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RequiredFieldComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
