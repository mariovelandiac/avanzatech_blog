import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { postCreateGuard } from './post-create.guard';

describe('postCreateGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) => 
      TestBed.runInInjectionContext(() => postCreateGuard(...guardParameters));

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
