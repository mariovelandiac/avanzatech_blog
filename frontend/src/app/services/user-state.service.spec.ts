import { TestBed } from '@angular/core/testing';

import { UserStateService } from './user-state.service';

describe('UserStateService', () => {
  let service: UserStateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UserStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should set userJustSignedUp', () => {
    // Arrange
    const user = {
      firstName: 'test',
      lastName: 'test',
    };
    // Act
    service.setUserJustSignUp(user);
    // Assert
    expect(service.getUserJustSignUp()).toEqual(user);
  });
});
