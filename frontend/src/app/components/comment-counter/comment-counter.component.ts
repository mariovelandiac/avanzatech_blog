import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommentList } from '../../models/interfaces/comment.interface';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-comment-counter',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './comment-counter.component.html',
  styleUrl: './comment-counter.component.sass'
})
export class CommentCounterComponent implements OnChanges {
  @Input() comments: CommentList | undefined
  @Input() postId: number | undefined;
  commentCounter = 0;
  commentPlural = 's';

  ngOnChanges(): void {
    if (this.comments && this.comments.count !== 0) {
      this.commentCounter = this.comments.count;
      this.commentPlural = this.commentCounter == 1 ? '' : 's ';
    }
  }

  get postDetailRoute(): string {
    return `/post/${this.postId}`;
  }
}
