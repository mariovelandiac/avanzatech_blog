import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnexpectedErrorComponent } from './unexpected-error.component';
import { faBug } from '@fortawesome/free-solid-svg-icons';

describe('UnexpectedErrorComponent', () => {
  let component: UnexpectedErrorComponent;
  let fixture: ComponentFixture<UnexpectedErrorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UnexpectedErrorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnexpectedErrorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display error message', () => {
    // Arrange
    const errorMessage = 'An unexpected error has occurred';
    component.errorMessage = errorMessage;
    // Act
    fixture.detectChanges();
    const compiled = fixture.nativeElement;
    // Assert
    expect(compiled.querySelector('h1').textContent).toContain(errorMessage);
  });

});
