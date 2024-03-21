import { LikeList, LikeListDTO } from "../models/interfaces/like.interface";
import { mockUserDTO } from "./user.model.mock";

export const mockLikeList: LikeList = {
  count: 15,
  likedBy: [
    {
      id: 1,
      firstName: 'John',
      lastName: 'Doe'
    },
    {
      id: 2,
      firstName: 'Jane',
      lastName: 'Doe'
    },
    {
      id: 3,
      firstName: 'John',
      lastName: 'Smith'
    },
    {
      id: 4,
      firstName: 'Jane',
      lastName: 'Smith'
    },
    {
      id: 5,
      firstName: 'Michael',
      lastName: 'Johnson'
    },
    {
      id: 6,
      firstName: 'Emily',
      lastName: 'Davis'
    },
    {
      id: 7,
      firstName: 'David',
      lastName: 'Brown'
    },
    {
      id: 8,
      firstName: 'Olivia',
      lastName: 'Miller'
    },
    {
      id: 9,
      firstName: 'Daniel',
      lastName: 'Wilson'
    },
    {
      id: 10,
      firstName: 'Sophia',
      lastName: 'Anderson'
    },
    {
      id: 11,
      firstName: 'Matthew',
      lastName: 'Taylor'
    },
    {
      id: 12,
      firstName: 'Ava',
      lastName: 'Thomas'
    },
    {
      id: 13,
      firstName: 'Andrew',
      lastName: 'Harris'
    },
    {
      id: 14,
      firstName: 'Emma',
      lastName: 'Clark'
    },
    {
      id: 15,
      firstName: 'Joseph',
      lastName: 'Lewis'
    }
  ]
}

export const mockLikeListDTO: LikeListDTO = {
  count: 15,
  next: null,
  previous: null,
  results: [
    {
      user: mockUserDTO,
      post: 2,
      is_active: false,
      id: 2
    },
    {
      user: mockUserDTO,
      post: 3,
      is_active: true,
      id: 3
    },
    {
      user: mockUserDTO,
      post: 4,
      is_active: false,
      id: 4
    },
    {
      user: mockUserDTO,
      post: 5,
      is_active: true,
      id: 5
    },
    {
      user: mockUserDTO,
      post: 6,
      is_active: false,
      id: 6
    },
    {
      user: mockUserDTO,
      post: 7,
      is_active: true,
      id: 7
    },
    {
      user: mockUserDTO,
      post: 8,
      is_active: false,
      id: 8
    },
    {
      user: mockUserDTO,
      post: 9,
      is_active: true,
      id: 9
    },
    {
      user: mockUserDTO,
      post: 10,
      is_active: false,
      id: 10
    },
    {
      user: mockUserDTO,
      post: 11,
      is_active: true,
      id: 11
    },
    {
      user: mockUserDTO,
      post: 12,
      is_active: false,
      id: 12
    },
    {
      user: mockUserDTO,
      post: 13,
      is_active: true,
      id: 13
    },
    {
      user: mockUserDTO,
      post: 14,
      is_active: false,
      id: 14
    },
    {
      user: mockUserDTO,
      post: 15,
      is_active: true,
      id: 15
    }
  ]
}


