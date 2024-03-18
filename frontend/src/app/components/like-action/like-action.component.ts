import { CommonModule } from '@angular/common';
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition, faHeart } from '@fortawesome/free-regular-svg-icons';
import { faHeart as faHeartSolid } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-like-action',
  standalone: true,
  imports: [CommonModule, FontAwesomeModule],
  templateUrl: './like-action.component.html',
  styleUrl: './like-action.component.sass'
})
export class LikeActionComponent implements OnChanges {
  @Input() isLiked: boolean | undefined = false;
  likeIcon: IconDefinition = faHeart;

  ngOnChanges(): void {
    this.likeIcon = this.isLiked ? faHeartSolid : faHeart;
  }

  like() {
    console.log("hello");
  }

}
