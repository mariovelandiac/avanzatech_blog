import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';
import { UserStateService } from '../../services/user-state.service';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-nav-bar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './nav-bar.component.html',
  styleUrl: './nav-bar.component.sass'
})
export class NavBarComponent implements OnInit {
  isAuthenticated: boolean = false;
  firstName: string = '';

  constructor(
    private authService: AuthService,
    private userStateService: UserStateService
  ) {}

  ngOnInit(): void {
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.firstName = isAuthenticated ? this.userStateService.getUser().firstName : '';
      this.isAuthenticated = isAuthenticated;
    });
  }
}
