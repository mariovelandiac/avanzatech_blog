import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable, catchError, map } from 'rxjs';
import { LikeDTO, LikeListDTO, LikedByUser, LikesByPost } from '../models/interfaces/like.interface';

@Injectable({
  providedIn: 'root'
})
export class LikeService {
  private likeEndpoint = `${environment.api}/like/`;
  private pageSize = 15;
  constructor(
    private httpService: HttpClient
  ) {}

  getLikesByPost(postId: string): Observable<LikeListDTO> {
    return this.httpService.get<LikeListDTO>(`${this.likeEndpoint}?post=${postId}&page_size=${this.pageSize}`)
  }

  getLikesByUserAndPost(postId: string, userId: string): Observable<boolean> {
    return this.httpService.get<LikeListDTO>(`${this.likeEndpoint}?post=${postId}&user=${userId}`)
    .pipe(map(response => Boolean(response.count)))
  }
}
