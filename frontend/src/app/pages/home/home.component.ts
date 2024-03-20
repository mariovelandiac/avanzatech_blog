import { Component } from '@angular/core';
import { NavBarComponent } from '../../components/nav-bar/nav-bar.component';
import { PostListComponent } from '../../components/post-list/post-list.component';
import { Title } from '@angular/platform-browser';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faSquarePlus } from '@fortawesome/free-regular-svg-icons';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [NavBarComponent, PostListComponent, FontAwesomeModule, RouterModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.sass'
})
export class HomeComponent {
  createPostIcon: IconDefinition = faSquarePlus;
  constructor(
    private titleService: Title,
    ) {
    this.titleService.setTitle('Home');
  }

  get createPostRoute(): string {
    return "/post/create"
  }
}
