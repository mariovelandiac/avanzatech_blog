import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AuthLinkComponent } from './auth-link.component';
import { RouterTestingModule } from '@angular/router/testing';

describe('AuthLinkComponent', () => {
  let component: AuthLinkComponent;
  let fixture: ComponentFixture<AuthLinkComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AuthLinkComponent, RouterTestingModule.withRoutes([])]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AuthLinkComponent);
    component = fixture.componentInstance;
    component.link = '/test';
    component.text = 'Test';
    component.action = 'Test';
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set a link to path being passed', () => {
    // Assert
    const link = fixture.nativeElement.querySelector('a');
    expect(link.getAttribute('href')).toBe(component.link);
  });

  it('should set a text to text being passed', () => {
    // Assert
    const span = fixture.nativeElement.querySelector('span');
    expect(span.textContent).toBe(component.text);
  });

  it('should set action as the the a tag text', () => {
    // Assert
    const link = fixture.nativeElement.querySelector('a');
    expect(link.textContent).toBe(component.action);
  });

  it('should be displayed only if link, text and action are set', () => {
    // Arrange
    component.link = '/test';
    component.text = 'Test';
    component.action = 'Test';
    // Act
    fixture.detectChanges();
    // Assert
    const container = fixture.nativeElement.querySelector('div');
    expect(container).toBeTruthy();
  });
});
