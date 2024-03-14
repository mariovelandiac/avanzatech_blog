import { TestBed } from '@angular/core/testing';
import { HttpInterceptor } from '@angular/common/http';

import { CsrfCookieInterceptor } from './cookie.interceptor';

describe('cookieInterceptor', () => {
  const interceptor: HttpInterceptor = new CsrfCookieInterceptor();

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(interceptor).toBeTruthy();
  });
});
