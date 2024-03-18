import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faTrashCan } from '@fortawesome/free-regular-svg-icons';

@Component({
  selector: 'app-delete-action',
  standalone: true,
  imports: [FontAwesomeModule],
  templateUrl: './delete-action.component.html',
  styleUrl: './delete-action.component.sass'
})
export class DeleteActionComponent {
  deleteIcon: IconDefinition = faTrashCan;
}
