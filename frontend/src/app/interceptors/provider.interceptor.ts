import { HTTP_INTERCEPTORS } from "@angular/common/http";
import { CsrfCookieInterceptor } from "./cookie.interceptor";

export const httpInterceptorProviders = [
  {
    provide: HTTP_INTERCEPTORS,
    useClass: CsrfCookieInterceptor,
    multi: true
  }
]
