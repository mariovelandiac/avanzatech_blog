import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LoginComponent } from './login.component';
import { SignUpService } from '../../services/sign-up.service';
import { UserStateService } from '../../services/user-state.service';
import { SignUpServiceStub } from '../../components/sign-up-form/sign-up-form.component.spec';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { mockUserGreetings } from '../../test-utils/login.mock';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;
  let signUpService: SignUpService;
  let userService: UserStateService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        {
          provide: SignUpService,
          useValue: jasmine.createSpyObj('SignUpService', ['getJustSignedUp'])
        },
        {
          provide: UserStateService,
          useValue: jasmine.createSpyObj('UserStateService', ['getUserJustSignUp'])
        }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    signUpService = TestBed.inject(SignUpService);
    userService = TestBed.inject(UserStateService);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show user greeting if user just signed up', () => {
    // Arrange
    component.justSignUp = true;
    // Act
    fixture.detectChanges();
    // Assert
    const element = fixture.nativeElement.querySelector('.green-sign')
    expect(element).toBeTruthy();
  });

  it('should not show user greeting if user did not just signed up', () => {
    // Arrange
    component.justSignUp = false;
    // Act
    fixture.detectChanges();
    // Assert
    const element = fixture.nativeElement.querySelector('.green-sign')
    expect(element).toBeFalsy();
  });

  it('should set justSingUp and user properties on Init', () => {
    // Arrange
    const user = mockUserGreetings;
    const signUpSpy = signUpService.getJustSignedUp as jasmine.Spy;
    const userSpy = userService.getUserJustSignUp as jasmine.Spy;
    signUpSpy.and.returnValue(true);
    userSpy.and.returnValue(user);
    // Act
    component.ngOnInit();
    // Assert
    expect(component.justSignUp).toBeTrue();
    expect(component.user).toEqual(user);
  })

  it('should set the title', () => {
    // Arrange
    const title = 'Log In';
    // Act & Assert
    expect(document.title).toBe(title)
  });
});
