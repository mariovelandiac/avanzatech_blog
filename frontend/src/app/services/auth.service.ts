import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private justSignedUpSubject = new BehaviorSubject<boolean>(false);
  justSignedUp$ = this.justSignedUpSubject.asObservable();
  constructor() { }

  setJustSignedUp(value: boolean) {
    this.justSignedUpSubject.next(value);
  }
}
