import { Injectable, inject } from '@angular/core';
import { CanActivate, CanActivateFn, Router, UrlTree } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable()
class AuthGuard  {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(): boolean | UrlTree {
    const authStatus = this.authService.getAuthentication();
    if (authStatus) {
      return true;
    }
    return this.router.parseUrl('/home');
  }
}

@Injectable()
class LoginSignUpGuard  {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(): boolean | UrlTree {
    const authStatus = this.authService.getAuthentication();
    if (authStatus) {
      return this.router.parseUrl('/home');
    }
    return true;
  }
}

export const postCreateGuard: CanActivateFn = (route, state) => {
  const authGuardInstance = new AuthGuard(inject(AuthService), inject(Router));
  return authGuardInstance.canActivate();
};

export const loginSignUpGuard: CanActivateFn = (route, state) => {
  const authGuardInstance = new LoginSignUpGuard(inject(AuthService), inject(Router));
  return authGuardInstance.canActivate();
};
