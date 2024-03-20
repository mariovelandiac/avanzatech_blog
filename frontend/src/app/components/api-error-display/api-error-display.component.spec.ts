import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApiErrorDisplayComponent } from './api-error-display.component';

describe('ApiErrorDisplayComponent', () => {
  let component: ApiErrorDisplayComponent;
  let fixture: ComponentFixture<ApiErrorDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ApiErrorDisplayComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ApiErrorDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render error message', () => {
    const error = 'Test error';
    component.errorMessage = error;
    fixture.detectChanges();
    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('p').textContent).toContain(error);
  })
});
