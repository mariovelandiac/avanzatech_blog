import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ReactiveFormsModule, Validators, ValidationErrors } from '@angular/forms';
import { RequiredFieldComponent } from '../required-field/required-field.component';
import { AuthLinkComponent } from '../auth-link/auth-link.component';

@Component({
  selector: 'app-sign-up-form',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, RequiredFieldComponent, AuthLinkComponent],
  templateUrl: './sign-up-form.component.html',
  styleUrl: './sign-up-form.component.sass'
})
export class SignUpFormComponent implements OnInit {
  signUpForm!: FormGroup;
  private strongPasswordRegex: RegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\.@$!%*?&])[A-Za-z\d\.@$!%*?&]{8,}$/;
  constructor(private formBuilder: FormBuilder) {}

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
  }

  onSubmit() {
    console.log(this.signUpForm.value);
  }

  checkPasswords(group: AbstractControl): ValidationErrors | null {
    const password = group.get('password')?.value;
    const confirmPassword = group.get('confirmPassword')?.value;
    return password === confirmPassword ? null : { notSame: true };
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
