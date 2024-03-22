import { Component, OnInit } from '@angular/core';
import { UnexpectedErrorComponent } from '../../components/unexpected-error/unexpected-error.component';
import { BackButtonComponent } from '../../components/back-button/back-button.component';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { PostRetrieve } from '../../models/interfaces/post.interface';
import { ActivatedRoute, Router } from '@angular/router';
import { PostService } from '../../services/post.service';
import { CommonModule, Location } from '@angular/common';
import { Title } from '@angular/platform-browser';
import { Category, CategoryDescription } from '../../models/enums/category.enum';
import { InversePermissionMap, PermissionDescription } from '../../models/enums/permission.enum';
import { PermissionFormComponent } from '../../components/permission-form/permission-form.component';
import { setCategoryPermissions } from '../../shared/utils';

@Component({
  selector: 'app-post-edit',
  standalone: true,
  imports: [
    UnexpectedErrorComponent,
    ReactiveFormsModule,
    BackButtonComponent,
    CommonModule,
    PermissionFormComponent
  ],
  templateUrl: './post-edit.component.html',
  styleUrl: './post-edit.component.sass'
})
export class PostEditComponent implements OnInit {
  post!: PostRetrieve;
  postId!: number;
  postForm!: FormGroup;
  publicPermission!: PermissionDescription;
  authenticatedPermission!: PermissionDescription;
  teamPermission!: PermissionDescription;
  ownerPermission!: PermissionDescription;
  wasAnError = false;
  errorMessage: string = '';
  successMessage: string = '';

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private postService: PostService,
    private formBuilder: FormBuilder,
    private title: Title,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.title.setTitle('Edit Post');
    this.route.paramMap.subscribe((params) => {
      this.postId = +params.get('id')!;
      this.fetchPost();
    });
  }

  fetchPost() {
    this.postService.retrieve(this.postId).subscribe({
      next: (post) => {
        this.post = post;
        this.setPermissions();
        this.buildForm();
        this.title.setTitle(this.title.getTitle() + ' - ' + this.post?.title);
      },
      error: (error) => {
        this.wasAnError = true;
        this.errorMessage = error;
      }
    });
  }

  setPermissions() {
    this.publicPermission = InversePermissionMap[this.post.category_permission.find((cp) => cp.category === Category.PUBLIC)?.permission!];
    this.authenticatedPermission = InversePermissionMap[this.post.category_permission.find((cp) => cp.category === Category.AUTHENTICATED)?.permission!];
    this.teamPermission = InversePermissionMap[this.post.category_permission.find((cp) => cp.category === Category.TEAM)?.permission!];
    this.ownerPermission = InversePermissionMap[this.post.category_permission.find((cp) => cp.category === Category.AUTHOR)?.permission!];
  }

  buildForm() {
    this.postForm = this.formBuilder.group({
      title: [this.post.title, [Validators.required]],
      content: [this.post.content, [Validators.required]]
    })
  }

  onSubmit() {
    const post = {
      id: this.postId,
      title: this.titleControl?.value as string,
      content: this.contentControl?.value as string,
      category_permission: setCategoryPermissions(this.postForm),
    };
    this.postService.update(post).subscribe({
      next: () => {
        this.successMessage = 'Post updated successfully';
        setTimeout(() => {
          this.router.navigate(['/post', this.postId]);
        }, 2000);
      },
      error: (error) => {
        this.wasAnError = true;
        this.errorMessage = error;
      }
    });
  }

  goBack() {
    this.router.navigate(['/home']);
  }

  onCancel() {
      this.location.back();
    }

  get titleControl() {
    return this.postForm.get('title');
  }

  get contentControl() {
    return this.postForm.get('content');
  }
}
