import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserStateService {

  private firstName: BehaviorSubject<string> = new BehaviorSubject<string>('');
  private lastName: BehaviorSubject<string> = new BehaviorSubject<string>('');
  firstName$ = this.firstName.asObservable();
  lastName$ = this.lastName.asObservable();

  constructor() { }

  setFirstName(value: string) {
    this.firstName.next(value);
  }

  getFirstName() {
    return this.firstName.getValue();
  }

  setLastName(value: string) {
    this.lastName.next(value);
  }

  getLastName() {
    return this.lastName.getValue();
  }

}
