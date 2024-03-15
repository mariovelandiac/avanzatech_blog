import { TestBed } from '@angular/core/testing';

import { UserStateService } from './user-state.service';
import { SignUpService } from './sign-up.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { mockLoginSuccessfulResponse } from '../test-utils/login.mock';
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
    const userDTO = mockLoginSuccessfulResponse;
    const user: User = {
      firstName: userDTO.first_name,
      lastName: userDTO.last_name,
      email: userDTO.email
    }
    // Act
    service.setUser(userDTO);
    // Assert
    expect(service.getUser()).toEqual(user);
    expect(localStorage.getItem('user')).toEqual(JSON.stringify(user));
  });

});
