import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { EditActionComponent } from './edit-action.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { RouterTestingModule } from '@angular/router/testing';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';

describe('EditActionComponent', () => {
  let component: EditActionComponent;
  let fixture: ComponentFixture<EditActionComponent>;
  let router: Router;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule.withRoutes([]), FontAwesomeModule],
      providers: []
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditActionComponent);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
