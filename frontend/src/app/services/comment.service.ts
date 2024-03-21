import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { CommentDTO, CommentList, CommentListDTO } from '../models/interfaces/comment.interface';
import { Pagination } from '../models/enums/constants.enum';

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  commentEndpoint = `${environment.api}/comment/`
  pageSize = Pagination.COMMENT_PAGE_SIZE;
  constructor(
    private httpService: HttpClient
  ) { }

  getCommentsByPost(postId: number, pageIndex: number = 0): Observable<CommentList> {
    const commentEndpoint = `${this.commentEndpoint}?page_size=${this.pageSize}&post=${postId}&page=${pageIndex + 1}`;
    return this.httpService.get<CommentListDTO>(commentEndpoint)
    .pipe(
      map((response) => this.transformComments(response))
    );
  }

  transformComments(response: CommentListDTO): CommentList {
    const count = response.count;
    const results = response.results.map((comment: CommentDTO) => ({
        id: comment.id,
        user: {
          firstName: comment.user.first_name,
          lastName: comment.user.last_name,
        },
        content: comment.content,
        createdAt: comment.created_at
      }));
    return { count, results };
  }

}
