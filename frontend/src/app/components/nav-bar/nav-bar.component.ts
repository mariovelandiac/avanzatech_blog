import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';
import { UserStateService } from '../../services/user-state.service';
import { Router, RouterModule } from '@angular/router';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faArrowRightFromBracket } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { TwoOptionsPopUpComponent } from '../two-options-pop-up/two-options-pop-up.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-nav-bar',
  standalone: true,
  imports: [CommonModule, RouterModule, FontAwesomeModule, TwoOptionsPopUpComponent],
  templateUrl: './nav-bar.component.html',
  styleUrl: './nav-bar.component.sass'
})
export class NavBarComponent implements OnInit {
  isAuthenticated: boolean = false;
  firstName: string = '';
  logoutIcon: IconDefinition = faArrowRightFromBracket;
  isIconDisabled: boolean = false;

  constructor(
    private authService: AuthService,
    private userStateService: UserStateService,
    private router: Router,
    private popUpService: MatDialog,
  ) {}

  ngOnInit(): void {
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.firstName = isAuthenticated ? this.userStateService.getUser().firstName : '';
      this.isAuthenticated = isAuthenticated;
    });
  }

  onLogout() {
    this.isIconDisabled = true;
    const dialog = this.popUpService.open(TwoOptionsPopUpComponent, {
      data: {
        title: 'Log Out',
        question: 'Are you sure you want to ' ,
        content: "logout",
        action: "Logout",
        hideCancel: false,
      },
    });
    dialog.afterClosed().subscribe((result) => {
      if (!result) {
        this.isIconDisabled = false;
        return;
      }
      this.logOut();
    });
  }

  logOut() {
    this.authService.logOut().subscribe({
      next: () => {
        this.router.navigate(['/']).then(() => {
          this.displayPopUp(true);
        })
      },
      error: () => {
        this.displayPopUp(false);
      }
    })
  }

  displayPopUp(success: boolean) {
    const data = {
      title: 'Log Out',
      question: '',
      content: success ? 'You have successfully logged out' : 'Failed to log out, please try again.',
      action: 'Ok',
      hideCancel: true,
    }
    this.popUpService.open(TwoOptionsPopUpComponent, {
      data: data
    });
  }
}
