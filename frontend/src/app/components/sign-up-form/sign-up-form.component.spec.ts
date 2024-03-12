import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SignUpFormComponent } from './sign-up-form.component';
import { ReactiveFormsModule } from '@angular/forms';
import { SignUpService } from '../../services/sign-up.service';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { formSignUp, requestSignUp, responseSignUp } from '../../models/interfaces/sign-up.interface';
import { of, throwError } from 'rxjs';


const successfulResponseMock = {
  id: 1,
  first_name: 'John',
  last_name: 'Doe',
  email: 'john.doe@example.com'
}
class SignUpServiceStub {
  public error = false;
  signUp(data: requestSignUp) {
    if (this.error) {
      return throwError(() => new Error('Sign up failed'))
    }
    return of(successfulResponseMock);
  }
}

describe('SignUpFormComponent', () => {
  let component: SignUpFormComponent;
  let fixture: ComponentFixture<SignUpFormComponent>;
  let signUpService: SignUpService;
  let authService: AuthService;
  let router: Router;

  beforeEach(async () => {
     await TestBed.configureTestingModule({
       imports: [ReactiveFormsModule],
       providers: [
         { provide: SignUpService, useClass: SignUpServiceStub },
         { provide: AuthService, useValue: jasmine.createSpyObj('AuthService', ['setJustSignedUp']) },
         { provide: Router, useValue: jasmine.createSpyObj('Router', ['navigate']) }
       ]
     }).compileComponents();

     fixture = TestBed.createComponent(SignUpFormComponent);
     component = fixture.componentInstance;
     signUpService = TestBed.inject(SignUpService);
     authService = TestBed.inject(AuthService);
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
  })

  it('should mark firstName as invalid if empty value', () => {
    // Arrange
    const firstNameControl = component.firstNameControl;
    // Act & Assert
    expect(firstNameControl?.hasError('required')).toBeTruthy();
  })

  it('should mark lastName as invalid if empty value', () => {
    // Arrange
    const lastNameControl = component.lastNameControl;
    // Act & Assert
    expect(lastNameControl?.hasError('required')).toBeTruthy();
  })

  it('should mark email as invalid if empty value', () => {
    // Arrange
    const emailControl = component.emailControl;
    // Act & Assert
    expect(emailControl?.hasError('required')).toBeTruthy();
  })

  it('should mark the email as invalid if it is not an email', () => {
    // Arrange
    const emailControl = component.emailControl;
    emailControl?.setValue('test');
    // Act & Assert
    expect(emailControl?.hasError('email')).toBeTruthy();
  })

  it('should mark password as invalid if empty value', () => {
    // Arrange
    const passwordControl = component.passwordControl;
    // Act & Assert
    expect(passwordControl?.hasError('required')).toBeTruthy();
  })

  it('should mark password as invalid if it does not match the regex', () => {
    // Arrange
    const passwordControl = component.passwordControl;
    passwordControl?.setValue('test');
    // Act & Assert
    expect(passwordControl?.hasError('pattern')).toBeTruthy();
  })

  it('should mark confirmPassword as invalid if empty value', () => {
    // Arrange
    const confirmPasswordControl = component.signUpForm.get('confirmPassword');
    // Act & Assert
    expect(confirmPasswordControl?.hasError('required')).toBeTruthy();
  })

  it('should mark confirmPassword as invalid if it does not match the password', () => {
    // Arrange
    const confirmPasswordControl = component.signUpForm.get('confirmPassword');
    const passwordControl = component.signUpForm.get('password');
    passwordControl?.setValue('not test');
    confirmPasswordControl?.setValue('test');
    // Act
    const result = component.checkPasswords(component.signUpForm)
    // Assert
    expect(result).toEqual({ notSame: true });
    expect(result).not.toBeNull();
  })

  it('should convert object keys firstName and lastName to snake case', () => {
    // Arrange
    const input: formSignUp = {
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com',
      password: 'testPassword',
      confirmPassword: 'testPassword'
    };
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
    spyOn(signUpService, 'signUp').and.returnValue(of(successfulResponseMock));

    // Act
    component.onSubmit();

    // Assert
    expect(signUpService.signUp).toHaveBeenCalled();
    expect(authService.setJustSignedUp).toHaveBeenCalledWith(true);
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
  })

});
