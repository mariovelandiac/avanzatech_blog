import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RequiredFieldComponent } from '../required-field/required-field.component';
import { Title } from '@angular/platform-browser';
import { AuthLinkComponent } from '../auth-link/auth-link.component';
import { ApiErrorDisplayComponent } from '../api-error-display/api-error-display.component';
import { UserDTO } from '../../models/interfaces/user.interface';
import { HttpErrorResponse } from '@angular/common/http';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition, faEye, faEyeSlash } from '@fortawesome/free-regular-svg-icons';
@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, RequiredFieldComponent, AuthLinkComponent, ApiErrorDisplayComponent, FontAwesomeModule],
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.sass'
})
export class LogInFormComponent implements OnInit {
  logInForm!: FormGroup;
  errorMessage: string = '';
  hidePassword: boolean = true;
  passwordIcon: IconDefinition = faEye;

  constructor(
    private router: Router,
    private formBuilder: FormBuilder,
    private title: Title,
    private authService: AuthService,
  ) {}

  ngOnInit() {
    this.title.setTitle('Log In');
    this.logInForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
    this.logInForm.valueChanges.subscribe(() => this.errorMessage = '');
  }

  onSubmit() {
    this.errorMessage = '';
    this.authService.logIn(this.logInForm.value).subscribe({
      next: (response: UserDTO) => {
        this.router.navigate(['/home']);
      },
      error: (error: HttpErrorResponse) => {
        this.errorMessage = error.message;
      }
    });
  }

  onCancel() {
    this.logInForm.reset();
  }

  togglePasswordVisibility() {
    this.hidePassword = !this.hidePassword;
    this.passwordIcon = this.hidePassword ? faEye : faEyeSlash;
  }

  get emailControl() {
    return this.logInForm.get('email');
  }

  get passwordControl() {
    return this.logInForm.get('password');
  }

  get passwordInput() {
    return this.hidePassword ? 'password' : 'text';
  }

}
