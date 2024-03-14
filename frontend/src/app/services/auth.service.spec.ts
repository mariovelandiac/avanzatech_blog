import { TestBed } from '@angular/core/testing';

import { AuthService } from './auth.service';
import { HttpClient } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { mockLoginSuccessfulResponse, mockLoginUser } from '../test-utils/login.mock';
import { environment } from '../../environments/environment.development';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthService]
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  })

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should log in successfully', () => {
    // Arrange
    const mockData = mockLoginUser;
    const mockSuccessfulResponse = mockLoginSuccessfulResponse;
    // Act & Arrange
    // Make the login http request
    service.logIn(mockData).subscribe((data) => {
      expect(data).toEqual(mockSuccessfulResponse);
    })
    // The following `expectOne()` will match the request's URL.
    const req = httpMock.expectOne(`${environment.api}/user/login/`);
    // Assert that the request is a POST.
    expect(req.request.method).toBe('POST');
    req.flush(mockSuccessfulResponse);
  });
  describe('isAuthenticated Behavior Subject', () => {
    it('should set authentication status', () => {
      // Arrange
      const isAuthenticated = true;
      // Act
      service.setAuthentication(isAuthenticated);
      // Assert
      service.isAuthenticated$.subscribe((data) => {
        expect(data).toBeTrue();
      });
    });

    it('should get authentication status when it changes', () => {
      // Arrange
      service.setAuthentication(true)
      // Act
      service.setAuthentication(false);
      // Assert
      service.isAuthenticated$.subscribe((data) => {
        expect(data).toBeFalse();
      });
    });
  });
  describe('Error handling', () => {


    it('Should handle HTTP error', () => {
      // Arrange
      const mockErrorResponse = {
        status: 400,
        error: {
          email: ['Email error'],
          password: ['Password error']
        }
      };
      // Act & Arrange
      // Make the login http request
      service.logIn(mockLoginUser).subscribe({
        next: () => {fail('should have failed')},
        error: (error) => {
          expect(error).toBeInstanceOf(Error);
          expect(error).toBeTruthy();
        }
      }
    );
    // The following `expectOne()` will match the request's URL.
    const req = httpMock.expectOne(`${environment.api}/user/login/`);
    // Assert that the request is a POST.
    expect(req.request.method).toBe('POST');
    // Respond with mock data, causing Observable to resolve.
    // Subscribe callback asserts that correct data was returned.
    req.flush(mockErrorResponse, {status: 400, statusText: 'Bad Request'});
  });

  it('should handle 403 error because of CSRF', () => {
    // Arrange
    const mockErrorResponse = {
      status: 403,
      error: {
        detail: 'CSRF error'
      }
    };
    // Act & Arrange
    // Make the login http request
    service.logIn(mockLoginUser).subscribe({
      next: () => {fail('should have failed')},
      error: (error) => {
        expect(error).toBeInstanceOf(Error);
        expect(error).toBeTruthy();
      }
    }
    );
    // The following `expectOne()` will match the request's URL.
    const req = httpMock.expectOne(`${environment.api}/user/login/`);
    // Assert that the request is a POST.
    expect(req.request.method).toBe('POST');
    // Respond with mock data, causing Observable to resolve.
    // Subscribe callback asserts that correct data was returned.
    req.flush(mockErrorResponse, {status: 403, statusText: 'Forbidden'});
  });

  it('should handle 403 error because of invalid email or password', () => {
    // Arrange
    const mockErrorResponse = {
      status: 403,
      error: {
        detail: 'Invalid email or password'
      }
    };
    // Act & Arrange
    // Make the login http request
    service.logIn(mockLoginUser).subscribe({
      next: () => {fail('should have failed')},
      error: (error) => {
        expect(error).toBeInstanceOf(Error);
        expect(error).toBeTruthy();
      }
    }
    );
    // The following `expectOne()` will match the request's URL.
    const req = httpMock.expectOne(`${environment.api}/user/login/`);
    // Assert that the request is a POST.
    expect(req.request.method).toBe('POST');
    // Respond with mock data, causing Observable to resolve.
    // Subscribe callback asserts that correct data was returned.
    req.flush(mockErrorResponse, {status: 403, statusText: 'Forbidden'});
  });

  it('should handle 500 status code', () => {
    // Arrange
    const mockErrorResponse = {
      status: 500,
      error: {
        detail: 'Internal server error'
      }
    };
    // Act & Arrange
    // Make the login http request
    service.logIn(mockLoginUser).subscribe({
      next: () => {fail('should have failed')},
      error: (error) => {
        expect(error).toBeInstanceOf(Error);
        expect(error).toBeTruthy();
      }
    }
    );
    // The following `expectOne()` will match the request's URL.
    const req = httpMock.expectOne(`${environment.api}/user/login/`);
    // Assert that the request is a POST.
    expect(req.request.method).toBe('POST');
    // Respond with mock data, causing Observable to resolve.
    // Subscribe callback asserts that correct data was returned.
    req.flush(mockErrorResponse, {status: 500, statusText: 'Internal Server Error'});
  });

  it('should handle 0 status code', () => {
    // Arrange
    const mockErrorResponse = {
      status: 0,
      error: {
        detail: 'Internal server error'
      }
    };
    // Act & Arrange
    // Make the login http request
    service.logIn(mockLoginUser).subscribe({
      next: () => {fail('should have failed')},
      error: (error) => {
        expect(error).toBeInstanceOf(Error);
        expect(error).toBeTruthy();
      }
    }
    );
    // The following `expectOne()` will match the request's URL.
    const req = httpMock.expectOne(`${environment.api}/user/login/`);
    // Assert that the request is a POST.
    expect(req.request.method).toBe('POST');
    // Respond with mock data, causing Observable to resolve.
    // Subscribe callback asserts that correct data was returned.
    req.flush(mockErrorResponse, {status: 0, statusText: 'Unknown Error'});
  });
});

});
