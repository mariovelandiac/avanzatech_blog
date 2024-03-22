import { CommentList, CommentListDTO } from "../models/interfaces/comment.interface";
import { mockUser, mockUserDTO } from "./user.model.mock";

export const mockCommentListDTO: CommentListDTO = {
  count: 1,
  next: null,
  previous: null,
  results: [
    {
      id: 1,
      content: "comment content",
      user: mockUserDTO,
      post: 1,
      is_active: true,
      created_at: "2021-08-10T00:00:00Z"
    },
    {
      id: 2,
      content: "comment content",
      user: mockUserDTO,
      post: 1,
      is_active: true,
      created_at: "2021-08-10T00:00:00Z"
    }
  ]
}

export const mockCommentList: CommentList = {
  count: 1,
  results: [
    {
      id: 1,
      content: "comment content",
      createdAt: "2021-08-10T00:00:00Z",
      user: mockUser
    }
  ]
}
