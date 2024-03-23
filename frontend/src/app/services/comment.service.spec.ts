import { TestBed } from '@angular/core/testing';

import { CommentService } from './comment.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { mockCommentList, mockCommentListDTO } from '../test-utils/comment.model.mock';

describe('CommentService', () => {
  let service: CommentService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });
    service = TestBed.inject(CommentService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get comments by post id', () => {
    // Arrange
    const postId = mockCommentListDTO.results[0].post;
    // Act
    service.getCommentsByPost(postId).subscribe((data) => {
      // Assert
      expect(data.count).toBe(mockCommentListDTO.count);
    });
    // Assert
    const req = httpMock.expectOne(`${service.commentEndpoint}?page_size=${service.pageSize}&post=${postId}&page=1`);
    expect(req.request.method).toBe('GET');
    req.flush(mockCommentListDTO);
  });
});
