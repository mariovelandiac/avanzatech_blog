import { BaseUser, UserPostDTO } from "./user.interface";

export interface Post {
  id: string;
  title: string;
  excerpt: string;
  createdAt: string;
  teamName: string;
  user: BaseUser;
  category_permission: category_permission[];
}

interface category_permission {
  category: string;
  permission: string;
}

export interface PostDTO {
  id: string;
  title: string;
  category_permission: category_permission[];
  user: UserPostDTO;
  excerpt: string;
  created_at: string;
}

export interface PostListDTO {
  count: string;
  next: string;
  previous: string;
  results: PostDTO[];
}


