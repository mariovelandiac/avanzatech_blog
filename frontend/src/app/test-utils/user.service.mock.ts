import { User, UserJustSignUp, UserLoginDTO } from "../models/interfaces/user.interface";
import { SignUpService } from "../services/sign-up.service";
import { mockUser } from "./user.model.mock";

export class mockUserStateService {
  private user!: User;

  constructor() {
    this.user = mockUser
  }

  getUser(): User {
    return this.user;
  }

  setUser(user: User): void {
    this.user = user;
  }

}
