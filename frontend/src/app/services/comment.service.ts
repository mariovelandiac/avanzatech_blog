import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CommentListDTO } from '../models/interfaces/comment.interface';

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  private commentEndpoint = `${environment.api}/comment/`
  private pageSize = 5;
  constructor(
    private httpService: HttpClient
  ) { }

  getCommentsByPost(postId: string): Observable<CommentListDTO> {
    return this.httpService.get<CommentListDTO>(`${this.commentEndpoint}?page_size=${this.pageSize}&post=${postId}`)
  }
}
