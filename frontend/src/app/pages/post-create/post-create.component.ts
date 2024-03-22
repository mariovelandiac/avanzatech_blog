import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { UnexpectedErrorComponent } from '../../components/unexpected-error/unexpected-error.component';
import { BackButtonComponent } from '../../components/back-button/back-button.component';
import { Title } from '@angular/platform-browser';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RequiredFieldComponent } from '../../components/required-field/required-field.component';
import { PermissionFormComponent } from '../../components/permission-form/permission-form.component';
import { PermissionDescription, PermissionMap } from '../../models/enums/permission.enum';
import { CategoriesAT, Category, CategoryDescription, CategoryMap } from '../../models/enums/category.enum';
import { PostService } from '../../services/post.service';
import { category_permission } from '../../models/interfaces/post.interface';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import { setCategoryPermissions } from '../../shared/utils';
import { MatDialog } from '@angular/material/dialog';
import { TwoOptionsPopUpComponent } from '../../components/two-options-pop-up/two-options-pop-up.component';

@Component({
  selector: 'app-post-create',
  standalone: true,
  imports: [
    CommonModule,
    UnexpectedErrorComponent,
    BackButtonComponent,
    ReactiveFormsModule,
    RequiredFieldComponent,
    PermissionFormComponent,
    RequiredFieldComponent
  ],
  templateUrl: './post-create.component.html',
  styleUrl: './post-create.component.sass'
})
export class PostCreateComponent implements OnInit {
  wasAnError = false;
  successMessage: string = '';
  errorMessage: string = '';
  postForm!: FormGroup;

  constructor(
    private title: Title,
    private formBuilder: FormBuilder,
    private postService: PostService,
    private router: Router,
    private location: Location,
    private popUpService: MatDialog
  ) {}

  ngOnInit(): void {
    this.title.setTitle('Create a Post');
    this.postForm = this.formBuilder.group({
      title: ['', [Validators.required]],
      content: ['', [Validators.required]],
    });
  }

  goBack() {
    this.router.navigate(['/home']);
  }

  onCancel() {
    this.location.back();
  }

  onSubmit() {
    const post = {
      title: this.titleControl?.value as string,
      content: this.contentControl?.value as string,
      category_permission: setCategoryPermissions(this.postForm)
    };
    this.postService.create(post).subscribe({
      next: (response) => {
        this.displayPopUp(true);
        this.postForm.reset();
        this.router.navigate(['/home']);

      },
      error: (error) => {
        this.errorMessage = error;
        this.wasAnError = true;
        this.displayPopUp(false);
      }
    })
  }

  displayPopUp(success: boolean) {
    const data = {
      title: 'Post creation',
      question: '',
      content: success ? `Post: ${this.titleControl!.value} has been created successfully` : 'Failed to create post, please try again.',
      action: 'Ok',
      hideCancel: true,
    }
    this.popUpService.open(TwoOptionsPopUpComponent, {
      data: data
    });
  }

  setCategoryPermissions(): category_permission[] {
    return CategoriesAT.map((category) => ({
      category: CategoryMap[category as keyof typeof CategoryMap],
      permission: PermissionMap[this.postForm.get(category)!.value as keyof typeof PermissionMap]
    }));
  }

  get titleControl() {
    return this.postForm.get('title');
  }

  get contentControl() {
    return this.postForm.get('content');
  };

  get readPermission() {
    return PermissionDescription.READ;
  }

  get editPermission() {
    return PermissionDescription.EDIT;
  }
 }
