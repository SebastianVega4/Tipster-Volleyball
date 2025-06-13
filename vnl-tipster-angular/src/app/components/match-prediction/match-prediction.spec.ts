import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MatchPrediction } from './match-prediction';

describe('MatchPrediction', () => {
  let component: MatchPrediction;
  let fixture: ComponentFixture<MatchPrediction>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatchPrediction]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MatchPrediction);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
