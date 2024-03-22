import { FormGroup } from "@angular/forms";
import { category_permission } from "../models/interfaces/post.interface";
import { CategoriesAT, CategoryMap } from "../models/enums/category.enum";
import { PermissionMap } from "../models/enums/permission.enum";

export const setCategoryPermissions = function(form: FormGroup): category_permission[] {
  return CategoriesAT.map((category) => ({
    category: CategoryMap[category as keyof typeof CategoryMap],
    permission: PermissionMap[form.get(category)!.value as keyof typeof PermissionMap]
  }));
}
