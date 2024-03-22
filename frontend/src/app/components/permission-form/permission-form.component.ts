import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { ControlContainer, FormControl, FormGroup, FormGroupDirective, ReactiveFormsModule, Validators } from '@angular/forms';
import { PermissionsAT } from '../../models/enums/permission.enum';

@Component({
  selector: 'app-permission-form',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './permission-form.component.html',
  styleUrl: './permission-form.component.sass',
  viewProviders: [{ provide: ControlContainer, useExisting: FormGroupDirective}]
})
export class PermissionFormComponent implements OnInit {
  @Input() category!: string;
  @Input() defaultPermission!: string;
  parentForm!: FormGroup;
  permissions = PermissionsAT;

  constructor(
    public postForm: FormGroupDirective
  ) {}

  ngOnInit(): void {
    this.parentForm = this.postForm.form;
    this.parentForm.addControl(this.category, new FormControl(this.defaultPermission, [Validators.required]));
  }

}
