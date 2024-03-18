import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommentListDTO } from '../../models/interfaces/comment.interface';
import { RouterModule } from '@angular/router';


@Component({
  selector: 'app-comment-counter',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './comment-counter.component.html',
  styleUrl: './comment-counter.component.sass'
})
export class CommentCounterComponent implements OnChanges {
  @Input() comments!: CommentListDTO | undefined
  private postId!: string;
  commentCounter = 0;
  commentPlural = 's';

  ngOnChanges(): void {
    if (this.comments && this.comments.results.length > 0) {
      this.commentCounter = +this.comments.count;
      this.commentPlural = this.commentCounter == 1 ? '' : 's ';
      this.postId = this.comments.results[0].post;
    }
  }
}
