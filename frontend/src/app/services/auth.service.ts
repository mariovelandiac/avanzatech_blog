import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, catchError, map, tap, throwError } from 'rxjs';
import { UserLoginDTO, UserLogIn } from '../models/interfaces/user.interface';
import { environment } from '../../environments/environment.development';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { UserStateService } from './user-state.service';
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private loginEndpoint = `${environment.api}/user/login/`;
  private logoutEndpoint = `${environment.api}/user/logout/`;
  private isAuthenticated = new BehaviorSubject<boolean>(false);
  isAuthenticated$ = this.isAuthenticated.asObservable();

  constructor(
    private httpService: HttpClient,
    private userService: UserStateService
    ) {
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

  logOut(): Observable<boolean> {
    return this.httpService.post(this.logoutEndpoint, {})
    .pipe(
      map(() => true),
      tap(() => this.clearAuth()),
      catchError(this.handleError)
    );
  }

  clearAuth() {
    this.setAuthentication(false);
    localStorage.removeItem('token');
    this.userService.clearUser();
  }

  handleError(error: HttpErrorResponse) {
    const internalError = 'An unexpected error occurred. Please try again later';
    let errorMessage = '';
    if (error.status == 400) {
      if (error.error.email)
        errorMessage += error.error.email[0] + '. ';
      else if (error.error.password)
        errorMessage += error.error.password[0] + '. ';
      else
        errorMessage = 'Invalid email or password';
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
    if (isAuthenticated) {
      localStorage.setItem('isAuthenticated', JSON.stringify(isAuthenticated));
    } else {
      localStorage.removeItem('isAuthenticated');
    }
  }

  getAuthentication(): boolean {
    return this.isAuthenticated.getValue();
  }

}
