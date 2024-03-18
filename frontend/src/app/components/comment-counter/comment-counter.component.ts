import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommentListDTO } from '../../models/interfaces/comment.interface';
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
  @Input() comments!: CommentListDTO | undefined
  private postId!: string;
  commentCounter = 0;
  commentPlural = 's';

  ngOnChanges(): void {
    if (this.comments && this.comments.count !== 0) {
      this.commentCounter = this.comments.count;
      this.commentPlural = this.commentCounter == 1 ? '' : 's ';
      // Storage post Id for routing in comment action component
      this.postId = this.comments.results[0].post;
    }
  }
}
