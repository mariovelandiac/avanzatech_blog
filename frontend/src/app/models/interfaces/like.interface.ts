import { BaseUser, UserDTO } from "./user.interface";

export interface LikeDTO {
  id: string,
  user: UserDTO,
  post: string,
  is_active: boolean
}

export interface LikeListDTO {
  count: number,
  next: string,
  previous: string,
  results: LikeDTO[]
}
export interface LikesByPost {
  likedBy: BaseUser[]
}

export interface LikedByUser {
  liked: boolean
}

export interface LikeCreateDTO {
  user: number,
  post: number
}
