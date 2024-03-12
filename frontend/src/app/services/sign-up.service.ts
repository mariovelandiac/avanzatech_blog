import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environment.development';
import { requestSignUp, responseSignUp } from '../models/interfaces/sign-up.interface';

@Injectable({
  providedIn: 'root'
})
export class SignUpService {
  private signUpEndpoint = `${environment.api}/user/sign-up/`
  constructor(private httpService: HttpClient) {}

  signUp(data: requestSignUp): Observable<responseSignUp> {
    // http headers
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    })
    return this.httpService.post<responseSignUp>(this.signUpEndpoint, data, { headers: headers })
    .pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = '';
    if (error.status == 400) {
      if (error.error.first_name)
        errorMessage += "First name " + error.error.first_name[0];
      if (error.error.last_name)
        errorMessage += "Last name " + error.error.last_name[0];
      if  (error.error.email)
        errorMessage += error.error.email[0];
      if (error.error.password)
        errorMessage += "Password " + error.error.password[0];
    }
    if (error.status == 500 || error.status == 0) {
      errorMessage = "An unexpected error occurred. Please try again later"
    }
    return throwError(() => new Error(errorMessage));
  }
}
