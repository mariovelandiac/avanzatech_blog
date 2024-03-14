import { Component, OnInit } from '@angular/core';
import { SignUpFormComponent } from '../../components/sign-up-form/sign-up-form.component';
import { Title } from '@angular/platform-browser';


@Component({
  selector: 'app-sign-up',
  standalone: true,
  imports: [SignUpFormComponent],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.sass'
})
export class SignUpComponent implements OnInit {
  private pageTitle = 'Sign Up'
  constructor(
    private title: Title
  ) {}

  ngOnInit() {
    this.title.setTitle(this.pageTitle);
  }

}
