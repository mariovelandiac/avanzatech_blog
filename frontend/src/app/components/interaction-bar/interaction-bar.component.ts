import { Component, Input } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition, faHeart, faComment, faPenToSquare, faTrashCan } from '@fortawesome/free-regular-svg-icons';
import { LikeActionComponent } from '../like-action/like-action.component';
import {
  faHeart as faHeartSolid,
  faComment as faCommentSolid,
  faPenToSquare as faPenToSquareSolid,
  faTrashCan as faTrashCanSolid
 } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-interaction-bar',
  standalone: true,
  imports: [FontAwesomeModule, LikeActionComponent],
  templateUrl: './interaction-bar.component.html',
  styleUrl: './interaction-bar.component.sass'
})
export class InteractionBarComponent {
  @Input() postId!: string;
  isLiked: boolean = false;
  commentIcon: IconDefinition = faComment;
  editIcon: IconDefinition = faPenToSquare;
  deleteIcon: IconDefinition = faTrashCan;
  isHover: boolean = false;
}
