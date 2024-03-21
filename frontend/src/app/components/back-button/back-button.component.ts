import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faChevronLeft } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-back-button',
  standalone: true,
  imports: [FontAwesomeModule],
  templateUrl: './back-button.component.html',
  styleUrl: './back-button.component.sass'
})
export class BackButtonComponent {
  backIcon: IconDefinition = faChevronLeft;
}
