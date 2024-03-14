import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { UserDTO, UserJustSignUp } from '../models/interfaces/user.interface';
import { SignUpService } from './sign-up.service';

@Injectable({
  providedIn: 'root'
})
export class UserStateService {
  private userJustSignedUp!: UserJustSignUp;
  private user!: UserDTO;

  constructor(
    private signUpService: SignUpService
  ) {}

  setUser(user: UserDTO) {
    this.user = user;
  }

  getUser() {
    return this.user;
  }

  setUserJustSignUp(user: UserJustSignUp) {
    this.userJustSignedUp = user;
  }

  getUserJustSignUp() {
    return this.userJustSignedUp;
  }

  clearUserJustSignUp() {
    this.signUpService.setJustSignedUp(false);
    this.userJustSignedUp = {
      firstName: '',
      lastName: '',
    };
  }

}
