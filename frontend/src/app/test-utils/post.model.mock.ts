import { Category } from '../models/enums/category.enum';
import { Permission } from '../models/enums/permission.enum';
import { Post } from '../models/interfaces/post.interface';

export const mockCreatedAtDTO = "2024-03-19T16:00:53.203928Z";
export const mockCreatedAt = "19/03/2024 11:00:53"

export const mockPost: Post = {
  id: 1,
  title: 'Test Post',
  excerpt: 'Test Post Excerpt',
  createdAt: mockCreatedAtDTO,
  user: {
    id: 1,
    firstName: 'Test',
    lastName: 'User',
    team: {
      id: 1,
      name: 'Test Team',
    },
  },
  category_permission: [
    {
      category: Category.PUBLIC,
      permission: Permission.READ,
    },
    {
      category: Category.AUTHENTICATED,
      permission: Permission.READ,
    },
    {
      category: Category.TEAM,
      permission: Permission.READ,
    },
    {
      category: Category.AUTHOR,
      permission: Permission.READ,
    },
  ],
  canEdit: false,
};
