import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TeamStats } from './team-stats';

describe('TeamStats', () => {
  let component: TeamStats;
  let fixture: ComponentFixture<TeamStats>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TeamStats]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TeamStats);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
