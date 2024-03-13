import { TestBed } from '@angular/core/testing';

import { UserStateService } from './user-state.service';

describe('UserStateService', () => {
  let service: UserStateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UserStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should set first name', () => {
    // Arrange
    const firstName = 'John';
    // Act
    service.setFirstName(firstName);
    // Assert
    expect(service.getFirstName()).toBe(firstName);
  });

  it('should set last name', () => {
    // Arrange
    const lastName = 'Doe';
    // Act
    service.setLastName(lastName);
    // Assert
    expect(service.getLastName()).toBe(lastName);
  });

  it('should get first name', () => {
    // Arrange
    const firstName = 'John';
    service.setFirstName(firstName);
    // Act
    const result = service.getFirstName();
    // Assert
    expect(result).toBe(firstName);
  });

  it('should get last name', () => {
    // Arrange
    const lastName = 'Doe';
    service.setLastName(lastName);
    // Act
    const result = service.getLastName();
    // Assert
    expect(result).toBe(lastName);
  });
});
