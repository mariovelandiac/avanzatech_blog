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
  first_name: string;
  last_name: string;
  email: string;
}
export interface User extends BaseUser {
  email: string;
}

export interface UserDTO {
  id: string;
  first_name: string;
  last_name: string;
  team: {
    id: string;
    name: string;
  };
}
