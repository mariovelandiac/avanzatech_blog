import { Component, Input } from '@angular/core';
import { Post, PostCommon } from '../../models/interfaces/post.interface';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-post-title-team-user',
  standalone: true,
  imports: [DatePipe],
  templateUrl: './post-title-team-user.component.html',
  styleUrl: './post-title-team-user.component.sass'
})
export class PostTitleTeamUserComponent {
  @Input() post: PostCommon | undefined;

  get id(): number {
    return this.post!.id;
  }

  get title(): string {
    return this.post!.title;
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

}
