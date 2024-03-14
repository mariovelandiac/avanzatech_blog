import { Injectable } from '@angular/core';
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class CsrfCookieInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Get the csrf token
    const csrfToken = this.getCSRFTokenFromCookie();
    // Modify the request
    const modifiedReq = req.clone({
      withCredentials: true, // Ensure credentials are sent with the request
      headers: req.headers.set('X-CSRFToken', csrfToken) // Replace cookie name
    });

    // Pass the modified request to the next handler
    return next.handle(modifiedReq);
  }

  private getCSRFTokenFromCookie(): string {
    const cookie = document.cookie.split(';');
    const csrfCookie = cookie.find(cookie => cookie.startsWith('csrftoken='));
    return csrfCookie ? csrfCookie.split('=')[1] : '';
  }
}
