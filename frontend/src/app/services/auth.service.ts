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
  private justSignedUp: boolean = false;
  private loginEndpoint = `${environment.api}/user/login/`;
  constructor(
    private userState: UserStateService,
    private httpService: HttpClient
    ) {}


  logIn(user: UserLogIn): Observable<UserDTO> {
    // setting http headers
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    return this.httpService.post<UserDTO>(this.loginEndpoint, user, {
      headers: headers,
      withCredentials: true
    })
      .pipe(
        catchError(this.handleError)
      );
  }

  handleError(error: HttpErrorResponse) {
    return throwError(() => new Error(error.message));
  }

  setJustSignedUp(value: boolean) {
    this.justSignedUp = value;
  }

  getJustSignedUp() {
    return this.justSignedUp;
  }

}
