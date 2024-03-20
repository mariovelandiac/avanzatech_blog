import { TestBed } from '@angular/core/testing';
import { HTTP_INTERCEPTORS, HttpClient, HttpInterceptor } from '@angular/common/http';
import { CsrfCookieInterceptor } from './cookie.interceptor';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('cookieInterceptor', () => {
  const interceptor: HttpInterceptor = new CsrfCookieInterceptor();
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        {
          provide: HTTP_INTERCEPTORS,
          useClass: CsrfCookieInterceptor,
          multi: true
        }
      ]
    });

    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(interceptor).toBeTruthy();
  });

  it('should add CSRF token to request', () => {
    // Arrange
    const httpClient = TestBed.inject(HttpClient);
    const expectedCsrfToken = 'test-csrf-token';
    document.cookie = `csrftoken=${expectedCsrfToken}`; // Simulate a CSRF token in the cookie

    // Act
    httpClient.get('/test').subscribe();

    // Assert
    const req = httpMock.expectOne('/test');
    expect(req.request.headers.get('X-CSRFToken')).toBe(expectedCsrfToken);
    expect(req.request.withCredentials).toBeTrue();
  });
});
