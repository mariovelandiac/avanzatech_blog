import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { UserStateService } from './user-state.service';
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private justSignedUp = new BehaviorSubject<boolean>(false);
  justSignedUp$ = this.justSignedUp.asObservable();
  constructor(
    private userState: UserStateService
    ) {}

  setJustSignedUp(value: boolean) {
    this.justSignedUp.next(value);
  }

  getJustSignedUp() {
    return this.justSignedUp.getValue();
  }

}
