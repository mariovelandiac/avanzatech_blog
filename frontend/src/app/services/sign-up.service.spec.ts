import { TestBed } from '@angular/core/testing';
import { SignUpService } from './sign-up.service';
import { HttpTestingController, HttpClientTestingModule } from '@angular/common/http/testing';
import { mockSignUpRequestData, mockSingUpSuccessResponse } from '../test-utils/sign-up.mock';
import { responseSignUp } from '../models/interfaces/sign-up.interface';
import { environment } from '../../environments/environment.development';
import { HttpErrorResponse } from '@angular/common/http';

describe('SignUpService', () => {
  let service: SignUpService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SignUpService]
    });
    service = TestBed.inject(SignUpService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  })

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should sign up successfully', () => {
    // Arrange
    const mockData = mockSignUpRequestData
    const mockResponseData = mockSingUpSuccessResponse
    // Act & Arrange
    // Make the signup http request
    service.signUp(mockData).subscribe((data) => {
      expect(data).toEqual(mockResponseData);
    })
    // The following `expectOne()` will match the request's URL.
    const req = httpMock.expectOne(`${environment.api}/user/sign-up/`);
      // Assert that the request is a POST.
    expect(req.request.method).toBe('POST');
    // Respond with mock data, causing Observable to resolve.
    // Subscribe callback asserts that correct data was returned.
    req.flush(mockResponseData);
  });

  it('Should handle HTTP error', () => {
    // Arrange
    const mockErrorResponse = {
      status: 400,
      error: {
        first_name: ['First name error'],
        last_name: ['Last name error'],
        email: ['Email error'],
        password: ['Password error']
      }
   };
    // Act & Arrange
    // Make the signup http request
    service.signUp(mockSignUpRequestData).subscribe({
      next: () => {fail('should have failed with 400 error')},
      error: (error) => {
        expect(error).toBeInstanceOf(Error);
        expect(error).toBeTruthy();
      }
    });
    // The following `expectOne()` will match the request's URL.
    const req = httpMock.expectOne(`${environment.api}/user/sign-up/`);
    // Assert that the request is a POST.
    expect(req.request.method).toBe('POST');
    // Respond with mock data, causing Observable to resolve.
    // Subscribe callback asserts that correct data was returned.
    req.flush(mockErrorResponse, { status: 400, statusText: 'Bad Request' });
  })

  it('should handle 400 status code with error payload', () => {
    // Arrange
    const errorResponse = new HttpErrorResponse({
      error: {
        first_name: ['Invalid first name'],
        last_name: ['Invalid last name'],
        email: ['Invalid email'],
        password: ['Invalid password']
      },
      status: 400
    });
    const expectedErrorMessage = 'First name Invalid first name. Last name Invalid last name. Invalid email. Password Invalid password. ';
    // Act y Arrange
    service.handleError(errorResponse).subscribe({
      error: (error) => {
        expect(error).toBeInstanceOf(Error),
        expect(error.message).toBe(expectedErrorMessage)
      }
    })
  });

  it('should handle 500 status code', () => {
    // Arrange
    const errorResponse = new HttpErrorResponse({ status: 500 });
    const expectedErrorMessage = 'An unexpected error occurred. Please try again later';
    // Act y Arrange
    service.handleError(errorResponse).subscribe({
      error: (error) => {
        expect(error).toBeInstanceOf(Error),
        expect(error.message).toBe(expectedErrorMessage)
      }
    })
  });

  it('should handle 0 status code', () => {
    // Arrange
    const errorResponse = new HttpErrorResponse({ status: 0 });
    const expectedErrorMessage = 'An unexpected error occurred. Please try again later';
    // Act y Arrange
    service.handleError(errorResponse).subscribe({
      error: (error) => {
        expect(error).toBeInstanceOf(Error),
        expect(error.message).toBe(expectedErrorMessage)
      }
    })
  });
});
