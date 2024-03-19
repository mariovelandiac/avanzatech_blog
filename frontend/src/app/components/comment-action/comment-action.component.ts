import { Component, Input } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faComment } from '@fortawesome/free-regular-svg-icons';

@Component({
  selector: 'app-comment-action',
  standalone: true,
  imports: [FontAwesomeModule, RouterModule],
  templateUrl: './comment-action.component.html',
  styleUrl: './comment-action.component.sass'
})
export class CommentActionComponent {
  @Input() postId: number | undefined;
  commentIcon: IconDefinition = faComment;

  get postDetailRoute(): string {
    return `/post/${this.postId}`;
  }
}
