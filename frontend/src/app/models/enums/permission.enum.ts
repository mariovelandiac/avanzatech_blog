export const enum Permission {
  READ = 1,
  EDIT = 2,
  NO_PERMISSION = 3
}

export const enum PermissionDescription {
  READ = 'Read Only',
  EDIT = 'Read & Write',
  NO_PERMISSION = 'None'
}


export const PermissionMap: Readonly<{[key in PermissionDescription]: Permission}> = {
  [PermissionDescription.READ]: Permission.READ,
  [PermissionDescription.EDIT]: Permission.EDIT,
  [PermissionDescription.NO_PERMISSION]: Permission.NO_PERMISSION
}

export const InversePermissionMap: Readonly<{[key in Permission]: PermissionDescription}> = {
  [Permission.READ]: PermissionDescription.READ,
  [Permission.EDIT]: PermissionDescription.EDIT,
  [Permission.NO_PERMISSION]: PermissionDescription.NO_PERMISSION
};

export const PermissionsAT: readonly string[] = Object.keys(PermissionMap);
