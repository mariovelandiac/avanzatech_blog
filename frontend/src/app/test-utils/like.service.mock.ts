import { Observable, of, throwError } from "rxjs";
import { LikeDTO, LikeList, LikeListDTO } from "../models/interfaces/like.interface";
import { HttpErrorResponse } from "@angular/common/http";
import { mockUserDTO } from "./user.model.mock";
import { mockTeam } from "./team.model.mock";

export class mockLikeService {
  constructor() {}

  getLikesByPost(postId: number, pageIndex: number = 0): Observable<LikeList> {
    return of({
      count: 1,
      likedBy: [
        {
          id: 1,
          firstName: 'Test',
          lastName: 'User'
        }
      ]
    });
  }

  getLikeByUserAndPost(postId: number, userId: number): Observable<boolean> {
    return of(true);
  }

  createLike(postId: number, userId: number): Observable<LikeDTO> {
    return of({
      id: 1,
      user: mockUserDTO,
      post: postId,
      is_active: true
    });
  }

  deleteLike(postId: number, userId: number): Observable<LikeDTO> {
    return of({
      id: 1,
      user: mockUserDTO,
      post: postId,
      is_active: true
    });
  }

  handleError(error: HttpErrorResponse): Observable<never> {
    return throwError(() => new Error(error.message));
  }

  transformLikeList(response: LikeListDTO): LikeList {
    const count = response.count;
    const likedBy = response.results.flatMap(like => ({
      id: like.user.id,
      firstName: like.user.first_name,
      lastName: like.user.last_name
    }));

    return { count, likedBy };
  }
}
