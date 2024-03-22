import { CommentList } from "./comment.interface";
import { LikeList } from "./like.interface";
import { UserDTO, UserRelated } from "./user.interface";

export interface category_permission {
  category: number;
  permission: number;
}
interface BasePost {
  id: number;
  title: string;
  category_permission: category_permission[];
}

interface BasePostDTO extends BasePost {
  created_at: string;
  user: UserDTO;
}

export interface PostDTO extends BasePostDTO {
  excerpt: string;
}

export interface PostCommon extends BasePost {
  createdAt: string;
  user: UserRelated;
  canEdit: boolean;
}

export interface Post extends PostCommon {
  excerpt: string;
  likes?: LikeList;
  comments?: CommentList;
  likedByAuthenticatedUser?: boolean;
}

export interface PostListDTO {
  count: number;
  next: string;
  previous: string;
  results: PostDTO[];
}

export interface PostList {
  posts: Post[];
  count: number;
}

export interface PostRetrieveDTO extends BasePostDTO {
  content: string;
}

export interface PostRetrieve extends PostCommon {
  content: string;
}


export interface PostCreateDTO {
  title: string;
  content: string;
  category_permission: category_permission[];
}
