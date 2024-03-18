import { Component, Input } from '@angular/core';
import { Post } from '../../models/interfaces/post.interface';
import { RouterModule } from '@angular/router';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-post-content',
  standalone: true,
  imports: [RouterModule, DatePipe],
  templateUrl: './post-content.component.html',
  styleUrl: './post-content.component.sass'
})
export class PostContentComponent {
  @Input() post!: Post;

  get title(): string {
    return this.post.title;
  }

  get excerpt(): string {
    return this.post.excerpt;
  }

  get createdAt(): string {
    return this.post.createdAt;
  }

  get team(): string {
    return this.post.teamName;
  }

  get user(): string {
    return `${this.post.user.firstName} ${this.post.user.lastName}`;
  }

  get id(): number {
    return this.post.id;
  }

  get postIdRoute(): string {
    return `/post/${this.id}`;
  }


}
