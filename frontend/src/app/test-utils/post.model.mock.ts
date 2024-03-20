import { Category } from '../models/enums/category.enum';
import { Permission } from '../models/enums/permission.enum';
import { Post } from '../models/interfaces/post.interface';

export const mockPost: Post = {
  id: 1,
  title: 'Test Post',
  excerpt: 'Test Post Excerpt',
  createdAt: new Date().toString(),
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
