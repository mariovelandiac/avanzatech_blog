import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { PostService } from './post.service';
import { mockPostList, mockPostListDTO } from '../test-utils/post.model.mock';

describe('PostService', () => {
  let service: PostService;
  let httpMock: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [PostService]
    });
    service = TestBed.inject(PostService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should list posts and return a PostList', () => {
    // Arrange
    const pageIndex = 0;
    // Act
    service.list(pageIndex).subscribe((data) => {
      expect(data.count).toBe(mockPostList.count);
      expect(data.posts).toEqual(mockPostList.posts);
    })
    // Assert
    const req = httpMock.expectOne(`${service.postEndpoint}?page=${pageIndex+1}&page_size=${service.pageSize}`);
    expect(req.request.method).toBe('GET');
    req.flush(mockPostListDTO);
  });

  it('should handle error on post list with status code 0', () => {
    // Arrange
    const pageIndex = 0;
    // Act
    service.list(pageIndex).subscribe({
      next: () => {fail('The request should have failed')},
      error: (error) => {
        expect(error).toBeInstanceOf(Error);
        expect(error.message).toBe('No internet connection');
      }
    }
    )
    // Assert
    const req = httpMock.expectOne(`${service.postEndpoint}?page=${pageIndex+1}&page_size=${service.pageSize}`);
    expect(req.request.method).toBe('GET');
    req.flush(null, { status: 0, statusText: 'No internet connection' });
  });

  it('should handle error on post list with status code 500', () => {
    // Arrange
    const pageIndex = 0;
    // Act
    service.list(pageIndex).subscribe({
      next: () => {fail('The request should have failed')},
      error: (error) => {
        expect(error).toBeInstanceOf(Error);
        expect(error.message).toBe('Error 500: Internal server error');
      }
    })
    // Assert
    const req = httpMock.expectOne(`${service.postEndpoint}?page=${pageIndex+1}&page_size=${service.pageSize}`);
    expect(req.request.method).toBe('GET');
    req.flush(null, { status: 500, statusText: 'Internal Server Error' });
  });

  it('should delete a post', () => {
    // Arrange
    const postId = 1;
    // Act
    service.delete(postId).subscribe();
    // Assert
    const req = httpMock.expectOne(`${service.postEndpoint}${postId}/`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
