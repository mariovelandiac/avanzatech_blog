import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, catchError, tap, throwError } from 'rxjs';
import { UserLoginDTO, UserLogIn } from '../models/interfaces/user.interface';
import { environment } from '../../environments/environment.development';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private loginEndpoint = `${environment.api}/user/login/`;
  private isAuthenticated = new BehaviorSubject<boolean>(false);
  isAuthenticated$ = this.isAuthenticated.asObservable();

  constructor(private httpService: HttpClient) {
      // Initialize the authentication status
      const storedAuth = localStorage.getItem('isAuthenticated');
      if (storedAuth)
        this.isAuthenticated.next(JSON.parse(storedAuth));
    }

  logIn(user: UserLogIn): Observable<UserLoginDTO> {
    // setting http headers
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.httpService.post<UserLoginDTO>(this.loginEndpoint, user, {
      headers: headers
    })
      .pipe(
        catchError(this.handleError)
      );
  }

  handleError(error: HttpErrorResponse) {
    const internalError = 'An unexpected error occurred. Please try again later';
    let errorMessage = '';
    if (error.status == 400) {
      if (error.error.email)
        errorMessage += error.error.email[0] + '. ';
      if (error.error.password)
        errorMessage += error.error.password[0] + '. ';
    }
    if (error.status == 500 || error.status == 0) {
      errorMessage = internalError;
    }
    if (error.status == 403) {
      if (error.error.detail.includes('CSRF')) {
        errorMessage = internalError;
      } else {
        errorMessage = 'Invalid email or password'
      }
    }
    return throwError(() => new Error(errorMessage));
  }

  setAuthentication(isAuthenticated: boolean) {
    this.isAuthenticated.next(isAuthenticated);
    localStorage.setItem('isAuthenticated', JSON.stringify(isAuthenticated));
  }

  getAuthentication(): boolean {
    return this.isAuthenticated.getValue();
  }

}
