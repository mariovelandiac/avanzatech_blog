import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CommentListDTO } from '../models/interfaces/comment.interface';
import { Pagination } from '../models/enums/constants.enum';

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  private commentEndpoint = `${environment.api}/comment/`
  private pageSize = Pagination.COMMENT_PAGE_SIZE;
  constructor(
    private httpService: HttpClient
  ) { }

  getCommentsByPost(postId: number): Observable<CommentListDTO> {
    return this.httpService.get<CommentListDTO>(`${this.commentEndpoint}?page_size=${this.pageSize}&post=${postId}`)
  }
}
