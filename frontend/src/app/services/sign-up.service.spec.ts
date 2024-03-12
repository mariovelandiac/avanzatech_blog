import { TestBed } from '@angular/core/testing';
import { SignUpService } from './sign-up.service';
import { HttpTestingController, HttpClientTestingModule } from '@angular/common/http/testing';

describe('SignUpService', () => {
  let service: SignUpService;
  let httpMock: HttpTestingController;



  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SignUpService]
    });
    service = TestBed.inject(SignUpService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
