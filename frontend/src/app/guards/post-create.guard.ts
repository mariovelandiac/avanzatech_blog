import { Injectable, inject } from '@angular/core';
import { CanActivateFn, Router, UrlTree } from '@angular/router';
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

export const postCreateGuard: CanActivateFn = (route, state) => {
  const authGuardInstance = new AuthGuard(inject(AuthService), inject(Router));
  return authGuardInstance.canActivate();
};
