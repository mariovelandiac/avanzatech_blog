import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable, ObservedValueOf, catchError, map, throwError } from 'rxjs';
import { Post, PostDTO, PostListDTO } from '../models/interfaces/post.interface';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  private postEndpoint = `${environment.api}/blog/`
  private pageSize = 10;
  constructor(
    private httpService: HttpClient
  ) {}

  list(): Observable<Post[]> {
    return this.httpService.get<PostListDTO>(`${this.postEndpoint}?page_size=${this.pageSize}`)
    .pipe(map((response) => {
      return response.results.map(this.transformPost);
    }))
  }

  delete(id: number): Observable<void> {
    return this.httpService.delete<void>(`${this.postEndpoint}${id}/`)
    .pipe(catchError(this.handleError));
  }

  handleError(error: any): Observable<never> {
    return throwError(() => new Error(error.message))
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
