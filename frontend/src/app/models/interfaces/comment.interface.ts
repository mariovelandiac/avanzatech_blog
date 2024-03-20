import { BaseUser, UserDTO } from "./user.interface";

export interface CommentDTO {
  id: number,
  content: string,
  user: UserDTO,
  post: number,
  is_active: boolean
  created_at: string
}

export interface CommentListDTO {
  count: number,
  next: string | null,
  previous: string | null,
  results: CommentDTO[]
}

