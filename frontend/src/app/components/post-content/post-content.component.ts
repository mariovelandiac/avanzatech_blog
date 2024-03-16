import { Component, Input } from '@angular/core';
import { LikeCounterComponent } from '../like-counter/like-counter.component';
import { CommentCounterComponent } from '../comment-counter/comment-counter.component';
import { InteractionBarComponent } from '../interaction-bar/interaction-bar.component';
import { Post } from '../../models/interfaces/post.interface';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-post-content',
  standalone: true,
  imports: [LikeCounterComponent, CommentCounterComponent, InteractionBarComponent, RouterModule],
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

  get id(): string {
    return this.post.id;
  }


}
