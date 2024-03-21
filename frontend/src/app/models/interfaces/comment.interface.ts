import { BaseUser, UserDTO } from "./user.interface";

interface BaseComment {
  id: number,
  content: string,
  post: number,
  is_active: boolean,
  created_at: string
}

interface CommentCommon {
  id: number,
  content: string,
  createdAt: string,
}

export interface CommentDTO extends BaseComment {
  user: UserDTO,
}

export interface CommentListDTO {
  count: number,
  next: string | null,
  previous: string | null,
  results: CommentDTO[]
}

export interface Comment extends CommentCommon {
  user: BaseUser
}

export interface CommentList {
  count: number,
  results: Comment[]
}

export interface CommentCreatedDTO extends BaseComment {
  user: number
}
export interface CommentCreated extends CommentCommon {
  user: number
}

