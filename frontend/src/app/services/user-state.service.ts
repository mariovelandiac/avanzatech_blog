import { Injectable } from '@angular/core';
import { User, UserLoginDTO, UserJustSignUp } from '../models/interfaces/user.interface';
import { SignUpService } from './sign-up.service';

@Injectable({
  providedIn: 'root'
})
export class UserStateService {
  private userJustSignedUp!: UserJustSignUp;
  private user!: User | null;

  constructor(private signUpService: SignUpService) {
    const storedUser = localStorage.getItem('user');
    if (storedUser)
      this.user = JSON.parse(storedUser);
  }

  setUser(user: UserLoginDTO) {
    this.user = this.toCamelCase(user);
    localStorage.setItem('user', JSON.stringify(this.user));
  }

  getUser(): User {
    return this.user!;
  }

  setUserJustSignUp(user: UserJustSignUp) {
    this.userJustSignedUp = user;
  }

  getUserJustSignUp() {
    return this.userJustSignedUp;
  }

  clearUser() {
    this.user = null;
    localStorage.removeItem('user');
  }

  clearUserJustSignUp() {
    this.signUpService.setJustSignedUp(false);
    this.userJustSignedUp = {
      firstName: '',
      lastName: '',
    };
  }

  private toCamelCase(user: UserLoginDTO): User {
    return {
      id: user.user_id,
      firstName: user.first_name,
      lastName: user.last_name,
      teamId: user.team_id,
      isAdmin: user.is_admin,
    };
  }

}
