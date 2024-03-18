import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
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
  @Output() likeClicked: EventEmitter<boolean> = new EventEmitter<boolean>();
  likeIcon: IconDefinition = faHeart;

  ngOnChanges(changes: SimpleChanges) {
    if (this.isLiked)
      this.setLikeButton(this.isLiked);
  }

  likeClick() {
    this.likeClicked.emit(this.isLiked);
  }

  setLikeButton(liked: boolean) {
    this.likeIcon = liked ? faHeartSolid : faHeart;
  }

}
