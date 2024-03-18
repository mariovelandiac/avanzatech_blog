import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable, map } from 'rxjs';
import { LikeListDTO, LikesByPost } from '../models/interfaces/like.interface';

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
}
