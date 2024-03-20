import { Component, EventEmitter, Input, OnChanges, Output } from '@angular/core';
import { LikeList, LikeListDTO } from '../../models/interfaces/like.interface';
import { UserLikedBy } from '../../models/interfaces/user.interface';
import { CommonModule } from '@angular/common';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { Pagination } from '../../models/enums/constants.enum';

@Component({
  selector: 'app-like-counter',
  standalone: true,
  imports: [CommonModule, MatPaginatorModule],
  templateUrl: './like-counter.component.html',
  styleUrl: './like-counter.component.sass'
})
export class LikeCounterComponent implements OnChanges {
  @Input() likes: LikeList | undefined;
  @Output() pageChange = new EventEmitter<number>();
  previousLikes: LikeList | undefined;
  showLikedBy: boolean = false;
  likeCounter = 0;
  likePlural = 's';
  previousPageIndex = 0;

  ngOnChanges() {
    if (!this.likes) return;
    this.likeCounter = this.likes.count;
    this.likePlural = this.likeCounter == 1 ? '' : 's';
    if (this.likes.count > this.pageSize) {
      this.likes.likedBy = this.likes.likedBy.slice(0, this.pageSize);
    }
  }

  showLikes(): void {
    if (!this.likes || !this.likeCounter) return;
    this.showLikedBy = !this.showLikedBy;
  }

  handlePageChange(e: PageEvent): void {
    const pageIndex = e.pageIndex;
    const moveForward = pageIndex > this.previousPageIndex;
    this.previousPageIndex = pageIndex;
    // Moving forward
    if (!this.previousLikes || moveForward) {
      this.previousLikes = this.likes;
      this.pageChange.emit(pageIndex);
    } else {
      // If the user is going backwards, use the previousLikes
      this.likes = this.previousLikes;
      this.previousLikes = undefined;
    }
  }

  get mousePointer() {
    return this.likeCounter ? 'pointer' : 'default';
  }

  get likedBy(): string[] {
    if (!this.likes) return [];
    return this.likes.likedBy.map((user: UserLikedBy) => `${user.firstName} ${user.lastName}`);
  }

  get pageSize() {
    return Pagination.LIKE_PAGE_SIZE;
  }

}
