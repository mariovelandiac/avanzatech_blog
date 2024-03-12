import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ReactiveFormsModule, Validators, ValidationErrors } from '@angular/forms';
import { RequiredFieldComponent } from '../required-field/required-field.component';
import { AuthLinkComponent } from '../auth-link/auth-link.component';
import { SignUpService } from '../../services/sign-up.service';
import { formSignUp, requestSignUp, responseSignUp } from '../../models/interfaces/sign-up.interface';
import { HttpErrorResponse } from '@angular/common/http';
import { ApiErrorDisplayComponent } from '../api-error-display/api-error-display.component';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-sign-up-form',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, RequiredFieldComponent, AuthLinkComponent, ApiErrorDisplayComponent],
  templateUrl: './sign-up-form.component.html',
  styleUrl: './sign-up-form.component.sass'
})
export class SignUpFormComponent implements OnInit {
  signUpForm!: FormGroup;
  private strongPasswordRegex: RegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\.@$!%*?&])[A-Za-z\d\.@$!%*?&]{8,}$/;
  errorMessage!: string;

  constructor(
    private formBuilder: FormBuilder,
    private signUpService: SignUpService,
    private authService: AuthService,
    private router: Router
    ) {}

  ngOnInit() {
    this.signUpForm = this.formBuilder.group({
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [
        Validators.required,
        Validators.pattern(this.strongPasswordRegex)]],
      confirmPassword: ['', Validators.required],
    }, { validators: this.checkPasswords });

    this.signUpForm.valueChanges.subscribe(() => this.errorMessage = '');
  }

  onSubmit() {
    const data = this.toSnakeCase(this.signUpForm.value)
    this.signUpService.signUp(data).subscribe({
      next: (response: responseSignUp) => {
        this.authService.setJustSignedUp(true);
        this.router.navigate(['/login']);
      },
      error: (error: HttpErrorResponse) => {
        this.errorMessage = error.message;
      }
    });
  }

  checkPasswords(group: AbstractControl): ValidationErrors | null {
    const password = group.get('password')?.value;
    const confirmPassword = group.get('confirmPassword')?.value;
    return password === confirmPassword ? null : { notSame: true };
  }

  private toSnakeCase(data: formSignUp): requestSignUp {
    return {
      first_name: data.firstName,
      last_name: data.lastName,
      ...data
    }
  }

  get firstNameControl() {
    return this.signUpForm.get('firstName');
  }

  get lastNameControl() {
    return this.signUpForm.get('lastName');
  }

  get emailControl() {
    return this.signUpForm.get('email');
  }

  get passwordControl() {
    return this.signUpForm.get('password');
  }

  get confirmPasswordControl() {
    return this.signUpForm.get('confirmPassword');
  }

  get hasUppercase(): boolean {
    return this.passwordControl?.value?.match(/(?=.*[A-Z])/) !== null;
  }

  get hasLowercase(): boolean {
    return this.passwordControl?.value?.match(/(?=.*[a-z])/) !== null;
   }

  get hasDigit(): boolean {
    return this.passwordControl?.value?.match(/.*[0-9].*/) !== null;
   }

  get hasSpecialCharacter(): boolean {
    return this.passwordControl?.value?.match(/(?=.*[\.!@#$%^&*])/) !== null;
   }

  get hasMinLength(): boolean {
    return this.passwordControl?.value?.length >= 8;
   }

}