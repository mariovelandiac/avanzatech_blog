import { Component, OnInit } from '@angular/core';
import { NavBarComponent } from '../../components/nav-bar/nav-bar.component';
import { PostListComponent } from '../../components/post-list/post-list.component';
import { Title } from '@angular/platform-browser';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faSquarePlus } from '@fortawesome/free-regular-svg-icons';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [NavBarComponent, PostListComponent, FontAwesomeModule, RouterModule, CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.sass'
})
export class HomeComponent implements OnInit {
  createPostIcon: IconDefinition = faSquarePlus;
  isAuthenticated: boolean = false;

  constructor(
    private titleService: Title,
    private authService: AuthService
    ) {}

    ngOnInit(): void {
    this.titleService.setTitle('Home');
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isAuthenticated = isAuthenticated;
    });
  }

  get createPostRoute(): string {
    return "/post/create"
  }
}
