import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable, catchError, map, throwError } from 'rxjs';
import { Post, PostList, PostDTO, PostListDTO } from '../models/interfaces/post.interface';
import { Pagination } from '../models/enums/constants.enum';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  private postEndpoint = `${environment.api}/blog/`
  private pageSize = Pagination.POST_PAGE_SIZE;

  constructor(
    private httpService: HttpClient
  ) {}

  list(pageIndex: number): Observable<PostList> {
    const postEndpointPaginated = `${this.postEndpoint}?page=${pageIndex + 1}&page_size=${this.pageSize}`;
    return this.httpService.get<PostListDTO>(postEndpointPaginated)
      .pipe(
        map(({ count, results }) => ({
          count,
          posts: results.map(this.transformPost)
        })),
        catchError(this.handleError)
      );
  }

  delete(id: number): Observable<void> {
    return this.httpService.delete<void>(`${this.postEndpoint}${id}/`)
    .pipe(catchError(this.handleError));
  }

  handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unexpected error has occurred';
    if (error.status === 0) {
      errorMessage = 'No internet connection';
    } else if (error.status !== 500) {
      errorMessage = `Something went wrong. Please try again later. Status code: ${error.status}.`;
    }
    return throwError(() => new Error(errorMessage))
  }

  transformPost(post: PostDTO): Post {
    return {
      id: post.id,
      title: post.title,
      excerpt: post.excerpt,
      createdAt: post.created_at,
      user: {
        id: post.user.id,
        firstName: post.user.first_name,
        lastName: post.user.last_name,
        team: {
          id: post.user.team.id,
          name: post.user.team.name
        }
      },
      category_permission: post.category_permission,
      canEdit: false
    }
  }


}
