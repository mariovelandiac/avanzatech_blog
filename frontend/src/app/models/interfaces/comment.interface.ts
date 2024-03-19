import { BaseUser, UserDTO } from "./user.interface";

export interface CommentDTO {
  id: number,
  content: number,
  user: UserDTO,
  post: number,
  is_active: boolean
  created_at: string
}

export interface CommentListDTO {
  count: number,
  next: string,
  previous: string,
  results: CommentDTO[]
}

