import {UserDTO, UserLikedBy} from "./user.interface";

export interface LikeDTO {
  id: number,
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
