import { Component, Input, OnChanges } from '@angular/core';
import { LikeListDTO } from '../../models/interfaces/like.interface';
import { BaseUser } from '../../models/interfaces/user.interface';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-like-counter',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './like-counter.component.html',
  styleUrl: './like-counter.component.sass'
})
export class LikeCounterComponent implements OnChanges {
  @Input() likes: LikeListDTO | undefined;
  likeCounter = 0;
  likePlural = 's';

  ngOnChanges() {
    if (this.likes) {
      this.likeCounter = +this.likes.count;
      this.likePlural = this.likeCounter == 1 ? '' : 's';
    }
  }

  showLikes(): void {
    const likedBy: string[] = []
    if (!this.likes) return;
    for (let like of this.likes.results) {
      likedBy.push(like.user.first_name + ' ' + like.user.last_name)
    }
    // TODO POPUP
    console.log(likedBy);
  }

}
