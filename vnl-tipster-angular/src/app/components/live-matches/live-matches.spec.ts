import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LiveMatches } from './live-matches';

describe('LiveMatches', () => {
  let component: LiveMatches;
  let fixture: ComponentFixture<LiveMatches>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LiveMatches]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LiveMatches);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
