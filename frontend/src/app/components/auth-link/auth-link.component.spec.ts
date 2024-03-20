import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AuthLinkComponent } from './auth-link.component';
import { RouterTestingModule } from '@angular/router/testing';

describe('AuthLinkComponent', () => {
  let component: AuthLinkComponent;
  let fixture: ComponentFixture<AuthLinkComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AuthLinkComponent, RouterTestingModule.withRoutes([])]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AuthLinkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
