import { Component, OnInit } from '@angular/core';
import { LogInFormComponent } from '../../components/login-form/login-form.component';
import { UserStateService } from '../../services/user-state.service';
import { AuthService } from '../../services/auth.service';
import { UserJustSignUp } from '../../models/interfaces/user.interface';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, LogInFormComponent],
  templateUrl: './login.component.html',
  styleUrl: './login.component.sass'
})
export class LoginComponent implements OnInit {
  justSignUp: boolean = false;
  user!: UserJustSignUp | undefined;

  constructor(
    private userState: UserStateService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.justSignUp = this.authService.getJustSignedUp();
    if (this.justSignUp)
      this.user = this.userState.getUserJustSignUp();
}

}
