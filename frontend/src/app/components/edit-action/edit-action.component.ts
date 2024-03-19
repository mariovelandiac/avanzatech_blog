import { Component, Input } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition, faPenToSquare } from '@fortawesome/free-regular-svg-icons';

@Component({
  selector: 'app-edit-action',
  standalone: true,
  imports: [FontAwesomeModule, RouterModule],
  templateUrl: './edit-action.component.html',
  styleUrl: './edit-action.component.sass'
})
export class EditActionComponent {
  @Input() postId!: number;
  editIcon: IconDefinition = faPenToSquare;

  get editUrl(): string {
    return `/post/edit/${this.postId}`;
  }
}
