import { TestBed } from '@angular/core/testing';

import { UserStateService } from './user-state.service';
import { SignUpService } from './sign-up.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { mockLoginSuccessfulResponse } from '../test-utils/user.model.mock';
import { User } from '../models/interfaces/user.interface';

describe('UserStateService', () => {
  let service: UserStateService;
  let signUpService: SignUpService;

  beforeEach(async () => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        {
          provide: SignUpService,
          useValue: jasmine.createSpyObj('SignUpService', ['setJustSignedUp'])
        }
      ]
    });

    service = TestBed.inject(UserStateService);
    signUpService = TestBed.inject(SignUpService);
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

  it('should clear userJustSignedUp', () => {
    // Arrange
    const user = {
      firstName: 'test',
      lastName: 'test',
    };

    // Act
    service.clearUserJustSignUp();
    // Assert
    expect(service.getUserJustSignUp()).toEqual({ firstName: '', lastName: '' });
    expect(signUpService.setJustSignedUp).toHaveBeenCalledWith(false);
  });

  it('should set user as User', () => {
    // Arrange
    const user = mockLoginSuccessfulResponse;
    const expectedUser: User = {
      id: user.user_id,
      firstName: user.first_name,
      lastName: user.last_name,
      teamId: user.team_id,
      isAdmin: user.is_admin,
    }
    // Act
    service.setUser(user);
    // Assert
    expect(service.getUser()).toEqual(expectedUser);
    expect(localStorage.getItem('user')).toEqual(JSON.stringify(expectedUser));
  });

});
