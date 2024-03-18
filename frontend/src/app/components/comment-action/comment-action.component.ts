import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faComment } from '@fortawesome/free-regular-svg-icons';

@Component({
  selector: 'app-comment-action',
  standalone: true,
  imports: [FontAwesomeModule],
  templateUrl: './comment-action.component.html',
  styleUrl: './comment-action.component.sass'
})
export class CommentActionComponent {
  commentIcon: IconDefinition = faComment;
}
