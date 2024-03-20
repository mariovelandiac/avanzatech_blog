import {UserDTO, UserLikedBy} from "./user.interface";

export interface LikeDTO {
  id: number,
  user: UserDTO,
  post: number,
  is_active: boolean
}

export interface LikeListDTO {
  count: number,
  next: string | null,
  previous: string | null,
  results: LikeDTO[]
}

export interface LikeList {
  count: number,
  likedBy: UserLikedBy[]
}

export interface LikedByUser {
  liked: boolean
}

export interface LikeCreateDTO {
  user: number,
  post: number
}
