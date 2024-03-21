import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommentActionComponent } from './comment-action.component';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';

describe('CommentActionComponent', () => {
  let component: CommentActionComponent;
  let fixture: ComponentFixture<CommentActionComponent>;
  let router: Router

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CommentActionComponent, RouterTestingModule.withRoutes([])]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CommentActionComponent);
    component = fixture.componentInstance;
    component.postId = 1;
    router = TestBed.inject(Router);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  it('should navigate to post detail page', () => {
    // Arrange
    const element = fixture.nativeElement.querySelector('fa-icon');
    const expectedRoute = component.postDetailRoute;
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
