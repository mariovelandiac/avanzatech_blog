export interface requestSignUp {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
}
export interface responseSignUp {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
}
export interface formSignUp {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
}

