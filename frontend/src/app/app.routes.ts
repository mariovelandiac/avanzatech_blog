import { Routes } from '@angular/router';
import { SignUpComponent } from './pages/sign-up/sign-up.component';
import { LoginComponent } from './pages/login/login.component';
import { HomeComponent } from './pages/home/home.component';
import { PostDetailComponent } from './pages/post-detail/post-detail.component';
import { PostEditComponent } from './pages/post-edit/post-edit.component';
import { PostCreateComponent } from './pages/post-create/post-create.component';

export const routes: Routes = [
  {
    path: 'signup',
    component: SignUpComponent,
  },
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: 'home',
    component: HomeComponent
  },
  {
    path: 'post/create',
    component: PostCreateComponent
  },
  {
    path: 'post/:id',
    component: PostDetailComponent
  },
  {
    path: 'post/edit/:id',
    component: PostEditComponent
  },
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: '**',
    redirectTo: '/home'
  }
];
