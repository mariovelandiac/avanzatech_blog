import { ComponentFixture, TestBed } from '@angular/core/testing';
import { faHeart as faHeartSolid } from '@fortawesome/free-solid-svg-icons';
import { faHeart } from '@fortawesome/free-regular-svg-icons';
import { LikeActionComponent } from './like-action.component';

describe('LikeActionComponent', () => {
  let component: LikeActionComponent;
  let fixture: ComponentFixture<LikeActionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LikeActionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LikeActionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set likeIcon to faHeartSolid when isLiked is true', () => {
    component.isLiked = true;
    component.ngOnChanges({});
    expect(component.likeIcon).toBe(faHeartSolid);
  });

  it('should set likeIcon to faHeart when isLiked is false', () => {
    component.isLiked = false;
    component.ngOnChanges({});
    expect(component.likeIcon).toBe(faHeart);
  });

  it('should emit likeClicked event when likeClick is called', () => {
    // Arrange
    component.isLiked = true;
    const spy = spyOn(component.likeClicked, 'emit') as jasmine.Spy;
    // Act
    component.likeClick();
    // Assert
    expect(spy).toHaveBeenCalled();
    expect(spy).toHaveBeenCalledWith(component.isLiked);
  });

});
