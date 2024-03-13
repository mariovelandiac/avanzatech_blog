import { TestBed } from '@angular/core/testing';

import { AuthService } from './auth.service';

describe('AuthService', () => {
  let service: AuthService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AuthService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });


  it('should set justSignedUp flag', () => {
    // Arrange
    const value = true;
    // Act
    service.setJustSignedUp(value);
    // Assert
    service.justSignedUp$.subscribe((result) => {
      expect(result).toEqual(value);
    });
  });

});
