import { TestBed } from '@angular/core/testing';

import { LikeService } from './like.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('LikeService', () => {
  let service: LikeService;
  let httpMock: HttpClientTestingModule

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [LikeService]
    });
    service = TestBed.inject(LikeService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
