import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { NgSelectOption } from '@angular/forms';
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
    this.isAuthenticated = this.authService.getAuthentication();
    this.firstName = this.isAuthenticated ? this.userStateService.getUser().firstName : '';
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isAuthenticated = isAuthenticated;
    });
  }
}
