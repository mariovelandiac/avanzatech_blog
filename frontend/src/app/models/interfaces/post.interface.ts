import { CommentListDTO } from "./comment.interface";
import { LikeList, LikeListDTO } from "./like.interface";
import { BaseUser, Team, UserDTO, UserRelated } from "./user.interface";

export interface Post {
  id: number;
  title: string;
  excerpt: string;
  createdAt: string;
  user: UserRelated;
  category_permission: category_permission[];
  canEdit: boolean;
  likes?: LikeList;
  comments?: CommentListDTO;
  likedByAuthenticatedUser?: boolean;
}

interface category_permission {
  category: number;
  permission: number;
}

export interface PostDTO {
  id: number;
  title: string;
  category_permission: category_permission[];
  user: UserDTO;
  excerpt: string;
  created_at: string;
}

export interface PostListDTO {
  count: number;
  next: string;
  previous: string;
  results: PostDTO[];
}


