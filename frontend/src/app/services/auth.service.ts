import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { UserStateService } from './user-state.service';
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private justSignedUp: boolean = false;
  constructor(
    private userState: UserStateService
    ) {}

  setJustSignedUp(value: boolean) {
    this.justSignedUp = value;
  }

  getJustSignedUp() {
    return this.justSignedUp;
  }

}
