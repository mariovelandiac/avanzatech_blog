import { Component, Input, OnChanges } from '@angular/core';
import { LikeList, LikeListDTO } from '../../models/interfaces/like.interface';
import { BaseUser, UserLikedBy } from '../../models/interfaces/user.interface';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-like-counter',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './like-counter.component.html',
  styleUrl: './like-counter.component.sass'
})
export class LikeCounterComponent implements OnChanges {
  @Input() likes: LikeList | undefined;
  likedBy: string[] = [];
  showLikedBy: boolean = false;
  likeCounter = 0;
  likePlural = 's';

  ngOnChanges() {
    if (this.likes) {
      this.likeCounter = +this.likes.count;
      this.likePlural = this.likeCounter == 1 ? '' : 's';
    }
  }

  showLikes(): void {
    if (!this.likes) return;
    this.likedBy = this.likes.likedBy.map((user: UserLikedBy) => `${user.firstName} ${user.lastName}`);
    this.showLikedBy = !this.showLikedBy;
  }

}
