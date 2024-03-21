import { Component, Input } from '@angular/core';
import { Post } from '../../models/interfaces/post.interface';
import { RouterModule } from '@angular/router';
import { CommonModule, DatePipe } from '@angular/common';

@Component({
  selector: 'app-post-excerpt',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './post-excerpt.component.html',
  styleUrl: './post-excerpt.component.sass'
})
export class PostExcerptComponent {
  @Input() postId!: number | undefined;
  @Input() excerpt!: string | undefined;
  private maxExcerptLength = 200;

  get displayShowMore(): boolean {
    return this.excerpt!.length >= this.maxExcerptLength;
  }

  get postDetailRoute(): string {
    return `/post/${this.postId}`;
  }

}
