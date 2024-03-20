import { Observable, of } from "rxjs";
import { CommentListDTO } from "../models/interfaces/comment.interface";
import { mockUserDTO } from "./user.model.mock";
import { HttpClient } from "@angular/common/http";

export class mockCommentService {

  constructor() { }
  getCommentsByPost(postId: number): Observable<CommentListDTO> {
    return of({
      count: 1,
      next: 'http://apidomain.com/api/comment/?page=2',
      previous: null,
      results: [{
        id: 1,
        content: "comment content",
        user: mockUserDTO,
        post: postId,
        is_active: true,
        created_at: (new Date()).toString()
      },]
    })
  }
}
