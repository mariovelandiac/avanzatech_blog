import { Component } from '@angular/core';
import { SignUpFormComponent } from '../../components/form-container/sign-up-form.component';


@Component({
  selector: 'app-sign-up',
  standalone: true,
  imports: [SignUpFormComponent],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.sass'
})
export class SignUpComponent {

}
