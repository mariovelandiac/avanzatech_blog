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

export const InverseCategoryMap: Readonly<{[key in Category]: CategoryDescription}> = {
  [Category.PUBLIC]: CategoryDescription.PUBLIC,
  [Category.AUTHENTICATED]: CategoryDescription.AUTHENTICATED,
  [Category.TEAM]: CategoryDescription.TEAM,
  [Category.AUTHOR]: CategoryDescription.OWNER,
};

export const CategoriesAT: readonly string[] = Object.keys(CategoryMap);

export const CategoriesId: ReadonlyArray<number> = Object.values(CategoryMap);
