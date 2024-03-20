import { BehaviorSubject, of, throwError } from "rxjs";
import { UserLoginDTO } from "../models/interfaces/user.interface";

export class MockAuthService {
  private isAuthenticated = new BehaviorSubject<boolean>(false);
  isAuthenticated$ = this.isAuthenticated.asObservable();

  constructor() {
     // Simulate the initialization of authentication status from localStorage
     const storedAuth = localStorage.getItem('isAuthenticated');
     if (storedAuth) {
       this.isAuthenticated.next(JSON.parse(storedAuth));
     }
  }

  logIn(user: any): any { // Adjust the type of 'user' as necessary
     // Simulate a successful login
     return of({} as UserLoginDTO); // Adjust the mock response as necessary
  }

  handleError(error: any): any {
     // Simulate error handling
     return throwError(() => new Error('Mock error message'));
  }

  setAuthentication(isAuthenticated: boolean): void {
     this.isAuthenticated.next(isAuthenticated);
     localStorage.setItem('isAuthenticated', JSON.stringify(isAuthenticated));
  }

  getAuthentication(): boolean {
     return this.isAuthenticated.getValue();
  }
 }
