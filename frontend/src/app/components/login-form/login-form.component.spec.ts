import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LogInFormComponent } from './login-form.component';
import { AuthService } from '../../services/auth.service';
import { RotateProp } from '@fortawesome/fontawesome-svg-core';
import { Router } from '@angular/router';
import { UserStateService } from '../../services/user-state.service';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { mockLoginSuccessfulResponse, mockLoginUser } from '../../test-utils/login.mock';
import { of } from 'rxjs';

describe('LogInFormComponent', () => {
  let component: LogInFormComponent;
  let fixture: ComponentFixture<LogInFormComponent>;
  let authService: AuthService;
  let userService: UserStateService;
  let router: Router;


  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReactiveFormsModule, HttpClientTestingModule],
      providers: [
        {
          provide: AuthService,
          useValue: jasmine.createSpyObj('AuthService', ['logIn', 'setAuthentication'])
        },
        {
          provide: UserStateService,
          useValue: jasmine.createSpyObj('UserStateService', ['clearUserJustSignUp', 'setUser'])
        },
        {
          provide: Router,
          useValue: jasmine.createSpyObj('Router', ['navigate'])
        }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LogInFormComponent);
    component = fixture.componentInstance;
    authService = TestBed.inject(AuthService);
    userService = TestBed.inject(UserStateService);
    router = TestBed.inject(Router);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('Should reset form fields on Cancel', () => {
    // Arrange
    const email = 'test@test.com';
    const password = 'test';
    component.logInForm.setValue({ email, password });
    // Act
    component.onCancel();
    // Assert
    expect(component.logInForm.value.email).toBeNull();
    expect(component.logInForm.value.password).toBeNull();
  });

  it('Should change password visibility', () => {
    // Arrange
    const passwordIcon = component.passwordIcon;
    const hidePassword = component.hidePassword;
    // Act
    component.togglePasswordVisibility();
    // Assert
    expect(component.passwordIcon).not.toEqual(passwordIcon);
    expect(component.hidePassword).not.toEqual(hidePassword);
  });

  it('Should change input type on password visibility toggle', () => {
    // Arrange
    const passwordInputType = component.passwordInput;
    // Act
    component.togglePasswordVisibility();
    // Assert
    expect(component.passwordInput).not.toEqual(passwordInputType);
    expect(component.passwordInput).toEqual('text');
  });

  it('Password input type should be password by default', () => {
    // Arrange & Act & Assert
    expect(component.passwordInput).toEqual('password');
  });


  describe('Form validation', () => {
    it('should create a form with two controls', () => {
      // Arrange & Act & Assert
      expect(component.logInForm.contains('email')).toBeTruthy();
      expect(component.logInForm.contains('password')).toBeTruthy();
    });

    it('should make the email control required', () => {
      // Arrange
      const control = component.logInForm.get('email');
      // Act
      control?.setValue('');
      // Assert
      expect(control?.valid).toBeFalsy();
    });

    it('should make the password control required', () => {
      // Arrange
      const control = component.logInForm.get('password');
      // Act
      control?.setValue('');
      // Assert
      expect(control?.valid).toBeFalsy();
    });

    it('should disable submit button if form is invalid', () => {
      // Arrange
      const button = fixture.nativeElement.querySelector('button[type="submit"]');
      const emailControl = component.logInForm.get('email');
      const passwordControl = component.logInForm.get('password');
      // Act
      emailControl?.setValue('');
      passwordControl?.setValue('');
      fixture.detectChanges();
      // Assert
      expect(button.disabled).toBeTruthy();
    });

    it('should clear error message on form value change', () => {
      // Arrange
      const errorMessage = 'Test error message';
      component.errorMessage = errorMessage;
      // Act
      component.logInForm.setValue({ email: 'test@test.com', password: 'test' });
      fixture.detectChanges();
      // Assert
      expect(component.errorMessage).toBe('');
    });
  });

  describe('Form Submission', () => {

    it('should call logIn method on form submit', () => {
      // Arrange
      component.logInForm.setValue(mockLoginUser);
      const authServiceSpy = authService.logIn as jasmine.Spy;
      authServiceSpy.and.returnValue(of(mockLoginSuccessfulResponse))
      // Act
      component.onSubmit();
      // Assert
      expect(authServiceSpy).toHaveBeenCalledWith(mockLoginUser);
    });

    it('should clean error message on submit click', () => {
      // Arrange
      const errorMessage = 'Test error message';
      component.errorMessage = errorMessage;
      component.logInForm.setValue(mockLoginUser);
      const authServiceSpy = authService.logIn as jasmine.Spy;
      authServiceSpy.and.returnValue(of(mockLoginSuccessfulResponse));
      // Act
      component.onSubmit();
      // Assert
      expect(component.errorMessage).toBe('');
    });

    it('should handle successful request', () => {
      // Arrange
      const mockUser = mockLoginUser;
      const authServiceSpy = authService.logIn as jasmine.Spy;
      authServiceSpy.and.returnValue(of(mockLoginSuccessfulResponse));
      // Act
      component.onSubmit();
      // Assert
      expect(userService.clearUserJustSignUp).toHaveBeenCalled();
      expect(userService.setUser).toHaveBeenCalledWith(mockLoginSuccessfulResponse);
      expect(authService.setAuthentication).toHaveBeenCalledWith(true);
      expect(router.navigate).toHaveBeenCalledWith(['/home']);
    });
  });
});
