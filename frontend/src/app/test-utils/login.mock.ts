import { UserDTO, UserLogIn } from "../models/interfaces/user.interface";

export const mockLoginUser: UserLogIn = {
  email: 'test@test.com',
  password: 'password'
}

export const mockLoginSuccessfulResponse: UserDTO = {
  first_name: 'Test',
  last_name: 'Test',
  email: mockLoginUser.email
}

export const mockUserGreetings = {
  firstName: 'Test',
  lastName: 'Test'
}
