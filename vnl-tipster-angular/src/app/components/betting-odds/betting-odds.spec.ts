import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BettingOdds } from './betting-odds';

describe('BettingOdds', () => {
  let component: BettingOdds;
  let fixture: ComponentFixture<BettingOdds>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BettingOdds]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BettingOdds);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
