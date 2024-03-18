import { BaseUser, UserDTO } from "./user.interface";

export interface LikeDTO {
  id: string,
  user: UserDTO,
  post: string,
  is_active: boolean
}

export interface LikeListDTO {
  count: string,
  next: string,
  previous: string,
  results: LikeDTO[]
}
export interface LikesByPost {
  likedBy: BaseUser[]
}
