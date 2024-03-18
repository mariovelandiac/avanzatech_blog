export interface BaseUser {
  firstName: string;
  lastName: string;
}

export interface UserJustSignUp extends BaseUser {}

export interface UserLogIn {
  email: string;
  password: string;
}
export interface UserLoginDTO {
  user_id: number;
  first_name: string;
  last_name: string;
  team_id: number;
  is_admin: boolean;
}
export interface User extends BaseUser {
  id: number;
  teamId: number;
  isAdmin: boolean;
}
export interface UserRelated extends BaseUser{
  id: number;
  team: Team;
}
export interface UserDTO {
  id: number;
  first_name: string;
  last_name: string;
  team: Team;
}

export interface UserLikedBy {
  id: number;
  firstName: string;
  lastName: string;
}

export interface Team {
  id: number;
  name: string;
}
