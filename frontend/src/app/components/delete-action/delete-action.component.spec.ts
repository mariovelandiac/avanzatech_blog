import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteActionComponent } from './delete-action.component';

describe('DeleteActionComponent', () => {
  let component: DeleteActionComponent;
  let fixture: ComponentFixture<DeleteActionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DeleteActionComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DeleteActionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
