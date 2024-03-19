import { Component, Input } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faBug } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-unexpected-error',
  standalone: true,
  imports: [FontAwesomeModule],
  templateUrl: './unexpected-error.component.html',
  styleUrl: './unexpected-error.component.sass'
})
export class UnexpectedErrorComponent {
  @Input() errorMessage: string = 'An unexpected error has occurred';
  errorIcon: IconDefinition = faBug;
}
