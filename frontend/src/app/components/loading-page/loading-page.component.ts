import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition, faSpinner } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-loading-page',
  standalone: true,
  imports: [FontAwesomeModule],
  templateUrl: './loading-page.component.html',
  styleUrl: './loading-page.component.sass'
})
export class LoadingPageComponent {
  loadingIcon: IconDefinition = faSpinner;
}
