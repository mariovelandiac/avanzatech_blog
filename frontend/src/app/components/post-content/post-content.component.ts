import { Component, Input } from '@angular/core';
import { Post } from '../../models/interfaces/post.interface';
import { RouterModule } from '@angular/router';
import { CommonModule, DatePipe } from '@angular/common';

@Component({
  selector: 'app-post-content',
  standalone: true,
  imports: [CommonModule, RouterModule, DatePipe],
  templateUrl: './post-content.component.html',
  styleUrl: './post-content.component.sass'
})
export class PostContentComponent {
  @Input() post!: Post | undefined;
  private maxExcerptLength = 200;

  get title(): string {
    this.post!.title = "hello world!0";
    return this.post!.title;
  }

  get excerpt(): string {
    return this.post!.excerpt;
  }

  get createdAt(): string {
    return this.post!.createdAt;
  }

  get team(): string {
    return this.post!.user.team.name;
  }

  get user(): string {
    return `${this.post!.user.firstName} ${this.post!.user.lastName}`;
  }

  get id(): number {
    return this.post!.id;
  }

  get postDetailRoute(): string {
    return `/post/${this.id}`;
  }

  get displayShowMore(): boolean {
    return this.excerpt.length >= this.maxExcerptLength;
  }


}
