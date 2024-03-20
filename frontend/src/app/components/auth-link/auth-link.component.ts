import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-auth-link',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './auth-link.component.html',
  styleUrl: './auth-link.component.sass'
})
export class AuthLinkComponent {
  @Input() text: string | undefined;
  @Input() link: string | undefined;
  @Input() action: string | undefined;

  get showAuthLink() {
    return this.link && this.text && this.action;
  }
}
