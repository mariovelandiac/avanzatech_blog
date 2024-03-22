import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogTitle } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { PopUpData } from '../../models/interfaces/common.interface';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-two-options-pop-up',
  standalone: true,
  imports: [MatDialogTitle, MatDialogContent, MatDialogActions, MatDialogClose, MatButtonModule, CommonModule],
  templateUrl: './two-options-pop-up.component.html',
  styleUrl: './two-options-pop-up.component.sass'
})
export class TwoOptionsPopUpComponent {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: PopUpData
  ) {}

  get title(): string {
    return this.data.title;
  }

  get question(): string {
    return this.data.question;
  }

  get action(): string {
    return this.data.action;
  }

  get content(): string {
    return this.data.content;
  }

  get showCancel(): boolean {
    return !this.data.hideCancel;
  }


}
