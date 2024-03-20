import { ComponentFixture, TestBed, tick, waitForAsync } from '@angular/core/testing';

import { NavBarComponent } from './nav-bar.component';
import { UserStateService } from '../../services/user-state.service';
import { AuthService } from '../../services/auth.service';
import { RouterTestingModule } from '@angular/router/testing';
import { Observable, of } from 'rxjs';
import { mockUser } from '../../test-utils/user.model.mock';
import { User } from '../../models/interfaces/user.interface';
import { Router } from '@angular/router';
import { MockAuthService } from '../../test-utils/auth.mock';

describe('NavBarComponent', () => {
  let component: NavBarComponent;
  let userStateService: UserStateService;
  let authService: AuthService;
  let router: Router;
  let fixture: ComponentFixture<NavBarComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule],
      providers: [
        {
          provide: UserStateService,
          useValue: jasmine.createSpyObj('UserStateService', [
            'getUser',
          ]),
        },
        {
          provide: AuthService,
          useClass: MockAuthService,
        },
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NavBarComponent);
    component = fixture.componentInstance;
    userStateService = TestBed.inject(UserStateService);
    authService = TestBed.inject(AuthService);
    (userStateService.getUser as jasmine.Spy).and.returnValue(mockUser);
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show first name if user is authenticated', () => {
    // Arrange
    authService.setAuthentication(true);
    const expectedText = `Welcome, ${mockUser.firstName}`;
    // Act
    fixture.detectChanges();
    // Assert
    const element = fixture.nativeElement.querySelector('#nav-action-container.nav-item h1');
    expect(element).toBeTruthy();
    expect(element.textContent).toBe(expectedText);
  });

  it('should not show greeting if user is not authenticated', () => {
    // Arrange
    authService.setAuthentication(false);
    // Act
    fixture.detectChanges();
    // Assert
    const element = fixture.nativeElement.querySelector('#nav-action-container.nav-item h1');
    expect(element).toBeFalsy();
  });

  it('should show action container if user is not authenticated', () => {
    // Arrange
    authService.setAuthentication(false);
    // Act
    fixture.detectChanges();
    // Assert
    const element = fixture.nativeElement.querySelector('#nav-action-container.nav-item div');
    expect(element).toBeTruthy();
  });

  it('should show login link if user is not authenticated', () => {
    // Arrange
    authService.setAuthentication(false);
    // Act
    fixture.detectChanges();
    // Assert
    const elements = fixture.nativeElement.querySelectorAll('#nav-action-container.nav-item a');
    console.log(elements);
    const loginLink = elements[0];
    expect(loginLink).toBeTruthy();
    expect(loginLink.innerText).toBe('Login');
    expect(loginLink.getAttribute('href')).toBe('/login');
  });

  it('should show register link if user is not authenticated', () => {
    // Arrange
    authService.setAuthentication(false);
    // Act
    fixture.detectChanges();
    // Assert
    const elements = fixture.nativeElement.querySelectorAll('#nav-action-container.nav-item a');
    const registerLink = elements[1];
    expect(registerLink).toBeTruthy();
    expect(registerLink.innerText).toBe('Register');
    expect(registerLink.getAttribute('href')).toBe('/signup');
  });
});
