import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NavBarComponent } from './nav-bar.component';
import { UserStateService } from '../../services/user-state.service';
import { AuthService } from '../../services/auth.service';
import { RouterTestingModule } from '@angular/router/testing';
import { of } from 'rxjs';

describe('NavBarComponent', () => {
  let component: NavBarComponent;
  let userStateService: UserStateService;
  let authService: AuthService;
  let fixture: ComponentFixture<NavBarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
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
          useValue: {
            isAuthenticated$: of(true),
          }
        },
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NavBarComponent);
    userStateService = TestBed.inject(UserStateService);
    authService = TestBed.inject(AuthService);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
