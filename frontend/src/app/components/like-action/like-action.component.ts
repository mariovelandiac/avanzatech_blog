import { Component, Input } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition, faHeart } from '@fortawesome/free-regular-svg-icons';
import { faHeart as faHeartSolid } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-like-action',
  standalone: true,
  imports: [FontAwesomeModule],
  templateUrl: './like-action.component.html',
  styleUrl: './like-action.component.sass'
})
export class LikeActionComponent {
  @Input() isLiked: boolean = false;
  likeIcon: IconDefinition = faHeart;

  like() {
    console.log("hello");
  }

}
