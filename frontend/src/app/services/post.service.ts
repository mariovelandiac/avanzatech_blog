import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable, ObservedValueOf, map } from 'rxjs';
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

  transformPost(post: PostDTO): Post {
    return {
      id: post.id,
      title: post.title,
      excerpt: post.excerpt,
      createdAt: post.created_at,
      teamName: post.user.team.name,
      user: {
        firstName: post.user.first_name,
        lastName: post.user.last_name
      },
      category_permission: post.category_permission
    }
  }


}
