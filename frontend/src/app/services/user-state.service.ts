import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { UserJustSignUp } from '../models/interfaces/user.interface';

@Injectable({
  providedIn: 'root'
})
export class UserStateService {

  private userJustSignedUp!: UserJustSignUp;

  constructor() { }

  setUserJustSignUp(user: UserJustSignUp) {
    this.userJustSignedUp = user;
  }

  getUserJustSignUp() {
    return this.userJustSignedUp;
  }

}
