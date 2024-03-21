import { TestBed } from '@angular/core/testing';

import { LikeService } from './like.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { mockLikeListDTO } from '../test-utils/like.model.mock';

describe('LikeService', () => {
  let service: LikeService;
  let httpMock: HttpTestingController

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

  it('should get likes by post and return a LikeList', () => {
    // Arrange
    const postId = 1;
    const pageIndex = 0;
    // Act
    service.getLikesByPost(postId, pageIndex).subscribe((data) => {
      expect(data.count).toBe(mockLikeListDTO.count);
      expect(data.likedBy).toEqual(mockLikeListDTO.results.map(like => ({
        id: like.user.id,
        firstName: like.user.first_name,
        lastName: like.user.last_name
      })));
    })
    // Assert
    const req = httpMock.expectOne(`${service.likeEndpoint}?post=${postId}&page_size=${service.pageSize}&page=${pageIndex+1}`);
    expect(req.request.method).toBe('GET');
    req.flush(mockLikeListDTO);
  });

  it('should get like by user and post and return a boolean', () => {
    // Arrange
    const postId = 1;
    const userId = 1;
    // Act
    service.getLikeByUserAndPost(postId, userId).subscribe((data) => {
      expect(data).toBeTrue();
    })
    // Assert
    const req = httpMock.expectOne(`${service.likeEndpoint}?post=${postId}&user=${userId}`);
    expect(req.request.method).toBe('GET');
    req.flush(mockLikeListDTO);
  });

  it('should get like by user and post and return false if count is 0', () => {
    // Arrange
    const postId = 1;
    const userId = 1;
    // Act
    service.getLikeByUserAndPost(postId, userId).subscribe((data) => {
      expect(data).toBeFalse();
    })
    // Assert
    const req = httpMock.expectOne(`${service.likeEndpoint}?post=${postId}&user=${userId}`);
    expect(req.request.method).toBe('GET');
    req.flush({ count: 0, results: [] });
  });

  it('should create a like and return a LikeDTO', () => {
    // Arrange
    const postId = 1;
    const userId = 1;
    // Act
    service.createLike(postId, userId).subscribe((data) => {
      expect(data).toEqual(mockLikeListDTO.results[0]);
    })
    // Assert
    const req = httpMock.expectOne(service.likeEndpoint);
    expect(req.request.method).toBe('POST');
    req.flush(mockLikeListDTO.results[0]);
  });

  it('should return an error when creating a like was not success', () => {
    // Arrange
    const postId = 1;
    const userId = 1;
    const mockErrorResponse = {
      status: 400,
      statusText: 'Bad Request'
    }
    // Act
    service.createLike(postId, userId).subscribe({
      error: (error) => {
        expect(error).toBeInstanceOf(Error);
        expect(error).toBeTruthy();
      }
    });
    // Assert
    const req = httpMock.expectOne(service.likeEndpoint);
    expect(req.request.method).toBe('POST');
    req.flush(null, mockErrorResponse);
  });

  it('should delete a like and return a LikeDTO', () => {
    // Arrange
    const postId = 1;
    const userId = 1;
    // Act
    service.deleteLike(postId, userId).subscribe((data) => {
      expect(data).toEqual(mockLikeListDTO.results[0]);
    })
    // Assert
    const req = httpMock.expectOne(`${service.likeEndpoint}${userId}/${postId}/`);
    expect(req.request.method).toBe('DELETE');
    req.flush(mockLikeListDTO.results[0]);
  });

  it('should return an error when deleting a like was not success', () => {
    // Arrange
    const postId = 1;
    const userId = 1;
    const mockErrorResponse = {
      status: 400,
      statusText: 'Bad Request'
    }
    // Act
    service.deleteLike(postId, userId).subscribe({
      error: (error) => {
        expect(error).toBeInstanceOf(Error);
        expect(error).toBeTruthy();
      }
    });
    // Assert
    const req = httpMock.expectOne(`${service.likeEndpoint}${userId}/${postId}/`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null, mockErrorResponse);
  });


});
