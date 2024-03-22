import { Routes } from '@angular/router';
import { SignUpComponent } from './pages/sign-up/sign-up.component';
import { LoginComponent } from './pages/login/login.component';
import { HomeComponent } from './pages/home/home.component';
import { PostDetailComponent } from './pages/post-detail/post-detail.component';
import { PostEditComponent } from './pages/post-edit/post-edit.component';
import { PostCreateComponent } from './pages/post-create/post-create.component';
import { LayoutComponent } from './pages/layout/layout.component';
import { postCreateGuard } from './guards/login-signup.guard';
import { loginSignupGuard } from './guards/login-signup.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: '',
    component: LayoutComponent,
    children: [
      {
        path: 'home',
        component: HomeComponent
      },
      {
        path: 'post/create',
        component: PostCreateComponent,
        canActivate: [postCreateGuard],
      },
      {
        path: 'post/:id',
        component: PostDetailComponent
      },
      {
        path: 'post/edit/:id',
        component: PostEditComponent
      },
    ]
  },
  {
    path: 'signup',
    component: SignUpComponent,
    canActivate: [loginSignupGuard],
  },
  {
    path: 'login',
    component: LoginComponent,
    canActivate: [loginSignupGuard],
  },

  {
    path: '**',
    redirectTo: '/home'
  }
];
