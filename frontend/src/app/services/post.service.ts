import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable, catchError, map, of, tap, throwError } from 'rxjs';
import { Post, PostList, PostDTO, PostListDTO, PostRetrieveDTO, PostRetrieve, PostCommon, PostCreateDTO, PostUpdateDTO } from '../models/interfaces/post.interface';
import { Pagination } from '../models/enums/constants.enum';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  postEndpoint = `${environment.api}/blog/`
  pageSize = Pagination.POST_PAGE_SIZE;
  cachedPosts: { [pageIndex: number]: PostList } = {}

  constructor(
    private httpService: HttpClient
  ) {}

  create(post: PostCreateDTO): Observable<boolean> {
    return this.httpService.post<PostDTO>(this.postEndpoint, post)
    .pipe(
      map(() => true),
      catchError(this.handleError)
    );
  }

  update(post: PostUpdateDTO): Observable<PostRetrieve> {
    return this.httpService.put<PostRetrieveDTO>(`${this.postEndpoint}${post.id}/`, post)
    .pipe(
      map(this.transformPostRetrieve),
      catchError(this.handleError)
    );
  }

  list(pageIndex: number): Observable<PostList> {
    if (this.cachedPosts[pageIndex]) {
      return of(this.cachedPosts[pageIndex]);
    }
    const postEndpointPaginated = `${this.postEndpoint}?page=${pageIndex + 1}&page_size=${this.pageSize}`;
    return this.httpService.get<PostListDTO>(postEndpointPaginated)
      .pipe(
        map(({ count, results }) => ({
          count,
          posts: results.map(this.transformPost)
        })),
        tap((posts) => this.cachedPosts[pageIndex] = posts),
        catchError(this.handleError)
      );
  }

  retrieve(id: number): Observable<PostRetrieve> {
    return this.httpService.get<PostRetrieveDTO>(`${this.postEndpoint}${id}/`)
      .pipe(
        map(this.transformPostRetrieve),
        catchError(this.handleError)
      );
  }

  delete(id: number): Observable<void> {
    return this.httpService.delete<void>(`${this.postEndpoint}${id}/`)
    .pipe(
      tap(() => {
        this.cachedPosts = {};
      }),
      catchError(this.handleError)
      );
  }

  handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage: string;
    const errorStatus = error.status;
    switch (errorStatus) {
      case 0:
        errorMessage = 'No internet connection';
        break;
      case 404:
        errorMessage = 'Error 404: Post not found';
        break;
      case 400:
        errorMessage = `Error 400: Bad request: ${error.error.detail}`;
        break;
      case 500:
        errorMessage = 'Error 500: Internal server error';
        break;
      default:
          errorMessage = `Something went wrong. Please try again later. Status code: ${errorStatus}.`;
        break;
    }
    return throwError(() => new Error(errorMessage))
  }

  transformPost(post: PostDTO): Post {
    return {
      id: post.id,
      title: post.title,
      category_permission: post.category_permission,
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
      canEdit: false,
      excerpt: post.excerpt,
    }
  }

  transformPostRetrieve(post: PostRetrieveDTO): PostRetrieve {
    return {
      id: post.id,
      title: post.title,
      category_permission: post.category_permission,
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
      canEdit: false,
      content: post.content
    }
  }

}
