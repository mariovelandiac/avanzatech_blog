
import { BaseUser, User, UserDTO, UserLogIn, UserLoginDTO } from "../models/interfaces/user.interface";
import { mockTeam } from "./team.model.mock";

export const mockLoginUser: UserLogIn = {
  email: 'test@test.com',
  password: 'password'
}

export const mockLoginSuccessfulResponse: UserLoginDTO = {
  user_id: 1,
  first_name: 'Test',
  last_name: 'Test',
  team_id: mockTeam.id,
  is_admin: false
}

export const mockUserGreetings: BaseUser = {
  firstName: 'Test',
  lastName: 'Test'
}

export const mockUserDTO: UserDTO = {
  id: 1,
  first_name: 'Test',
  last_name: 'Test',
  team: mockTeam,
}

export const mockUser: User  = {
  id: 1,
  firstName: 'Test',
  lastName: 'Test',
  teamId: mockTeam.id,
  isAdmin: false
}

export const mockBaseUser: BaseUser = {
  firstName: 'Test',
  lastName: 'Test'
}


