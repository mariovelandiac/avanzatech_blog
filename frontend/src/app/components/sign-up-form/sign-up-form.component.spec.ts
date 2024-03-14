import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SignUpFormComponent } from './sign-up-form.component';
import { ReactiveFormsModule } from '@angular/forms';
import { SignUpService } from '../../services/sign-up.service';
import { Router } from '@angular/router';
import { formSignUp, requestSignUp,} from '../../models/interfaces/sign-up.interface';
import { of, throwError } from 'rxjs';
import { mockFormSignUp, mockSingUpSuccessResponse } from '../../test-utils/sign-up.mock';
import { UserStateService } from '../../services/user-state.service';

export class SignUpServiceStub {
  public error = false;
  signUp(data: requestSignUp) {
    if (this.error) {
      return throwError(() => new Error('Sign up failed'));
    }
    return of(mockSingUpSuccessResponse);
  }
  setJustSignedUp(value: boolean) {
    return;
  }
}

describe('SignUpFormComponent', () => {
  let component: SignUpFormComponent;
  let fixture: ComponentFixture<SignUpFormComponent>;
  let signUpService: SignUpService;
  let userService: UserStateService;
  let router: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReactiveFormsModule],
      providers: [
        { provide: SignUpService, useClass: SignUpServiceStub },
        {
          provide: UserStateService,
          useValue: jasmine.createSpyObj('UserStateService', [
            'setUserJustSignUp',
          ]),
        },
        {
          provide: Router,
          useValue: jasmine.createSpyObj('Router', ['navigate']),
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(SignUpFormComponent);
    component = fixture.componentInstance;
    signUpService = TestBed.inject(SignUpService);
    userService = TestBed.inject(UserStateService);
    router = TestBed.inject(Router);
    fixture.detectChanges();
  });

  it('should create the component', () => {
    // Arrange & Act & Assert
    expect(component).toBeTruthy();
  });

  it('should create the form', () => {
    // Arrange & Act & Assert
    expect(component.signUpForm).toBeTruthy();
  });

  describe('Form Validation', () => {
    it('should mark firstName as invalid if empty value', () => {
      // Arrange
      const firstNameControl = component.firstNameControl;
      // Act & Assert
      expect(firstNameControl?.hasError('required')).toBeTruthy();
    });

    it('should mark lastName as invalid if empty value', () => {
      // Arrange
      const lastNameControl = component.lastNameControl;
      // Act & Assert
      expect(lastNameControl?.hasError('required')).toBeTruthy();
    });

    it('should mark email as invalid if empty value', () => {
      // Arrange
      const emailControl = component.emailControl;
      // Act & Assert
      expect(emailControl?.hasError('required')).toBeTruthy();
    });

    it('should mark the email as invalid if it is not an email', () => {
      // Arrange
      const emailControl = component.emailControl;
      emailControl?.setValue('test');
      // Act & Assert
      expect(emailControl?.hasError('email')).toBeTruthy();
    });

    it('should mark password as invalid if empty value', () => {
      // Arrange
      const passwordControl = component.passwordControl;
      // Act & Assert
      expect(passwordControl?.hasError('required')).toBeTruthy();
    });

    it('should mark password as invalid if it does not match the regex', () => {
      // Arrange
      const passwordControl = component.passwordControl;
      passwordControl?.setValue('test');
      // Act & Assert
      expect(passwordControl?.hasError('pattern')).toBeTruthy();
    });

    it('should mark confirmPassword as invalid if empty value', () => {
      // Arrange
      const confirmPasswordControl =
        component.signUpForm.get('confirmPassword');
      // Act & Assert
      expect(confirmPasswordControl?.hasError('required')).toBeTruthy();
    });

    it('should mark confirmPassword as invalid if it does not match the password', () => {
      // Arrange
      const confirmPasswordControl =
        component.signUpForm.get('confirmPassword');
      const passwordControl = component.signUpForm.get('password');
      passwordControl?.setValue('not test');
      confirmPasswordControl?.setValue('test');
      // Act
      const result = component.checkPasswords(component.signUpForm);
      // Assert
      expect(result).toEqual({ notSame: true });
      expect(result).not.toBeNull();
    });
  });

  describe('Form Submission', () => {
    it('should convert object keys firstName and lastName to snake case', () => {
      // Arrange
      const input: formSignUp = mockFormSignUp
      // Act
      const result = component.toSnakeCase(input);
      // Assert
      expect(result).toEqual({
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@example.com',
        password: 'testPassword',
      });
    });

    it('should handle successful sign up', () => {
      // Arrange
      const requestSignUpMock = {
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@example.com',
        password: 'testPassword',
      };
      spyOn(signUpService, 'signUp').and.returnValue(
        of(mockSingUpSuccessResponse)
      );

      spyOn(signUpService, 'setJustSignedUp');

      // Act
      component.onSubmit();

      // Assert
      expect(signUpService.signUp).toHaveBeenCalled();
      expect(signUpService.setJustSignedUp).toHaveBeenCalledWith(true);
      expect(userService.setUserJustSignUp).toHaveBeenCalledWith(
        {
          firstName: requestSignUpMock.first_name,
          lastName: requestSignUpMock.last_name,
        });
      expect(router.navigate).toHaveBeenCalledWith(['/login']);
    });

    it('should handle sign up error', () => {
      // Arrange
      const error = new Error('Sign up failed');
      spyOn(signUpService, 'signUp').and.returnValue(throwError(() => error));

      // Act
      component.onSubmit();

      // Assert
      expect(signUpService.signUp).toHaveBeenCalled();
      expect(component.errorMessage).toEqual('Sign up failed');
    });

    it('should clear errorMessage on form value change', () => {
      // Arrange
      component.errorMessage = 'Error message';

      // Act
      const email = component.signUpForm.get('email');
      email!.setValue('test@example.com');
      fixture.detectChanges();

      // Assert
      expect(component.errorMessage).toBe('');
   });

  });
  describe('Getters test', () => {

    it('should return the firstName control', () => {
      // Arrange
      const expectedControl = component.signUpForm.get('firstName');
      // Act
      const firstNameControl = component.firstNameControl;
      // Assert
      expect(firstNameControl).toBe(expectedControl);
    });

    it('should return the lastName control', () => {
      // Arrange
      const expectedControl = component.signUpForm.get('lastName');
      // Act
      const lastNameControl = component.lastNameControl;
      // Assert
      expect(lastNameControl).toBe(expectedControl);
    });

    it('should return the email control', () => {
      // Arrange
      const expectedControl = component.signUpForm.get('email');
      // Act
      const emailControl = component.emailControl;
      // Assert
      expect(emailControl).toBe(expectedControl);
    });

    it('should return the password control', () => {
      // Arrange
      const expectedControl = component.signUpForm.get('password');
      // Act
      const passwordControl = component.passwordControl;
      // Assert
      expect(passwordControl).toBe(expectedControl);
    });

    it('should return the confirmPassword control', () => {
      // Arrange
      const expectedControl = component.signUpForm.get('confirmPassword');
      // Act
      const confirmPasswordControl = component.confirmPasswordControl;
      // Assert
      expect(confirmPasswordControl).toBe(expectedControl);
    });
  })
});
