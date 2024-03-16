import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition, faHeart, faComment, faPenToSquare, faTrashCan } from '@fortawesome/free-regular-svg-icons';
@Component({
  selector: 'app-interaction-bar',
  standalone: true,
  imports: [FontAwesomeModule],
  templateUrl: './interaction-bar.component.html',
  styleUrl: './interaction-bar.component.sass'
})
export class InteractionBarComponent {
  likeIcon: IconDefinition = faHeart;
  commentIcon: IconDefinition = faComment;
  editIcon: IconDefinition = faPenToSquare;
  deleteIcon: IconDefinition = faTrashCan;

}
