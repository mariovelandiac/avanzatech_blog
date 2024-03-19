import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogTitle } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { Post } from '../../models/interfaces/post.interface';

@Component({
  selector: 'app-post-delete-dialog',
  standalone: true,
  imports: [MatDialogTitle, MatDialogContent, MatDialogActions, MatDialogClose, MatButtonModule],
  templateUrl: './post-delete-dialog.component.html',
  styleUrl: './post-delete-dialog.component.sass'
})
export class PostDeleteDialogComponent {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { title: Post['title'] },
  ) {}

}
