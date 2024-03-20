import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable, catchError, map, throwError } from 'rxjs';
import { LikeCreateDTO, LikeDTO, LikeList, LikeListDTO } from '../models/interfaces/like.interface';
import { Pagination } from '../models/enums/constants.enum';

@Injectable({
  providedIn: 'root'
})
export class LikeService {
  private likeEndpoint = `${environment.api}/like/`;
  private pageSize = Pagination.LIKE_PAGE_SIZE;
  constructor(
    private httpService: HttpClient
  ) {}

  getLikesByPost(postId: number, pageIndex: number = 0): Observable<LikeList> {
    const likeEndpointPaginated = `${this.likeEndpoint}?post=${postId}&page_size=${this.pageSize}&page=${pageIndex+1}`;
    return this.httpService.get<LikeListDTO>(likeEndpointPaginated)
    .pipe(map((response) => this.transformLikeList(response)));
  }

  getLikeByUserAndPost(postId: number, userId: number): Observable<boolean> {
    return this.httpService.get<LikeListDTO>(`${this.likeEndpoint}?post=${postId}&user=${userId}`)
    .pipe(map(response => Boolean(response.count)))
  }

  createLike(postId: number, userId: number): Observable<LikeDTO> {
    const body: LikeCreateDTO = {
      user: userId,
      post: postId
    }
    return this.httpService.post<LikeDTO>(this.likeEndpoint, body).pipe(catchError(this.handleError));
  }

  deleteLike(postId: number, userId: number): Observable<LikeDTO> {
    return this.httpService.delete<LikeDTO>(`${this.likeEndpoint}${userId}/${postId}/`).pipe(catchError(this.handleError));
  }

  handleError(error: HttpErrorResponse): Observable<never> {
      return throwError(() => new Error(error.message))
  }

  transformLikeList(response: LikeListDTO): LikeList {
    const count = response.count;
    const likedBy = response.results.flatMap(like => ({
      id: like.user.id,
      firstName: like.user.first_name,
      lastName: like.user.last_name,
    }));

    return { count, likedBy };
  }
}
