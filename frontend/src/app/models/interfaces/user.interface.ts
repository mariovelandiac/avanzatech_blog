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
  email: string;
  team_id: string;
}
export interface User extends BaseUser {
  id: number;
  email: string;
  teamId: Team["id"];
}

export interface UserDTO {
  id: number;
  first_name: string;
  last_name: string;
  team: Team;
}

interface Team {
  id: string;
  name: string;
}
