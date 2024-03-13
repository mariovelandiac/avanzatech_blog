import { formSignUp, requestSignUp, responseSignUp } from "../models/interfaces/sign-up.interface";

export const mockFormSignUp: formSignUp = {
  firstName: 'John',
  lastName: 'Doe',
  email: 'john.doe@example.com',
  password: 'testPassword',
  confirmPassword: 'testPassword',
};

export const mockSingUpSuccessResponse: responseSignUp = {
  id: 1,
  first_name: 'John',
  last_name: 'Doe',
  email: 'john.doe@example.com',
}

export const mockSignUpRequestData: requestSignUp = {
  first_name: 'John',
  last_name: 'Doe',
  email: 'john@doe.com',
  password: 'testPassword',
}
