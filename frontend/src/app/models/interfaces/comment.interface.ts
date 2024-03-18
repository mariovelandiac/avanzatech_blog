import { BaseUser, UserDTO } from "./user.interface";

export interface CommentDTO {
  id: string,
  content: string,
  user: UserDTO,
  post: string,
  is_active: boolean
  created_at: string
}

export interface CommentListDTO {
  count: string,
  next: string,
  previous: string,
  results: CommentDTO[]
}

