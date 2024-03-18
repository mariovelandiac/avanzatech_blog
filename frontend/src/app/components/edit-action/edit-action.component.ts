import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition, faPenToSquare } from '@fortawesome/free-regular-svg-icons';

@Component({
  selector: 'app-edit-action',
  standalone: true,
  imports: [FontAwesomeModule],
  templateUrl: './edit-action.component.html',
  styleUrl: './edit-action.component.sass'
})
export class EditActionComponent {
  editIcon: IconDefinition = faPenToSquare;
}
