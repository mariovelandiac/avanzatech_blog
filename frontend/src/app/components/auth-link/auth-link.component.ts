import { Component, Input } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-auth-link',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './auth-link.component.html',
  styleUrl: './auth-link.component.sass'
})
export class AuthLinkComponent {
  @Input() text!: string;
  @Input() link!: string;
  @Input() action!: string;
}
