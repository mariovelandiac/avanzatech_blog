export const enum Category {
  PUBLIC = 1,
  AUTHENTICATED = 2,
  TEAM = 3,
  AUTHOR = 4,
}
export const enum CategoryDescription {
  PUBLIC = 'Public',
  AUTHENTICATED = 'Authenticated',
  TEAM = 'Team',
  OWNER = 'Owner',
}
export const CategoryMap: Readonly<{[key in CategoryDescription]: Category}> = {
  [CategoryDescription.PUBLIC]: Category.PUBLIC,
  [CategoryDescription.AUTHENTICATED]: Category.AUTHENTICATED,
  [CategoryDescription.TEAM]: Category.TEAM,
  [CategoryDescription.OWNER]: Category.AUTHOR,
};

export const CategoriesAT: readonly string[] = Object.keys(CategoryMap);
