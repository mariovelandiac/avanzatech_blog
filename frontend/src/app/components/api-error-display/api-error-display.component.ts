import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-api-error-display',
  standalone: true,
  imports: [],
  templateUrl: './api-error-display.component.html',
  styleUrl: './api-error-display.component.sass'
})
export class ApiErrorDisplayComponent {
  @Input() errorMessage!: string;
}
