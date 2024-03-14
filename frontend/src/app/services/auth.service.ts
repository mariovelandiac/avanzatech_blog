import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, catchError, throwError } from 'rxjs';
import { UserStateService } from './user-state.service';
import { UserDTO, UserLogIn } from '../models/interfaces/user.interface';
import { environment } from '../../environments/environment.development';
import { AnyCatcher } from 'rxjs/internal/AnyCatcher';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private loginEndpoint = `${environment.api}/user/login/`;
  private isAuthenticated = new BehaviorSubject<boolean>(false);
  isAuthenticated$ = this.isAuthenticated.asObservable();

  constructor(
    private userState: UserStateService,
    private httpService: HttpClient
    ) {}


  logIn(user: UserLogIn): Observable<UserDTO> {
    // setting http headers
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.httpService.post<UserDTO>(this.loginEndpoint, user, {
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
  }

}
