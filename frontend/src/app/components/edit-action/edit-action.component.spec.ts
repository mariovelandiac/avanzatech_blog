import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { EditActionComponent } from './edit-action.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { RouterTestingModule } from '@angular/router/testing';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { concatMap } from 'rxjs';

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
    component.postId = 1;
    router = TestBed.inject(Router);
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should navigate to edit page', () => {
    // Arrange
    const element = fixture.nativeElement.querySelector('fa-icon');
    const expectedRoute = component.editUrl;
    const spy = spyOn(router, 'navigate');
    const navigateByUrlSpy = spyOn(router, 'navigateByUrl') as jasmine.Spy;
    // Act
    element.click();
    // Assert
    const navArgs = navigateByUrlSpy.calls.first().args[0];
    expect(router.navigateByUrl).toHaveBeenCalled();
    expect(expectedRoute).toContain(navArgs);
  });
});
