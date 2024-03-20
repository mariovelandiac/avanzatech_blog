import { HttpErrorResponse } from "@angular/common/http";
import { Observable, of, throwError } from "rxjs";
import { Post, PostDTO, PostList } from "../models/interfaces/post.interface";
import { Category } from "../models/enums/category.enum";
import { Permission } from "../models/enums/permission.enum";
import { mockPost } from "./post.model.mock";

export class mockPostService {

  constructor() {}

  list(pageIndex: number): Observable<PostList> {
    return of({
      count: 1,
      posts: [
        mockPost,
      ]
    });
  }

  delete(id: number): Observable<void> {
    return of();
  }

  handleError(error: HttpErrorResponse): Observable<never> {
    return throwError(() => new Error('An unexpected error has occurred'));
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
