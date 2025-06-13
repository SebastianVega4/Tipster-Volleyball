import { Component, OnInit, Input } from '@angular/core';
import { PredictionService } from '../../services/prediction';
import { Prediction } from '../../models/prediction.model';

@Component({
  selector: 'app-match-prediction',
  templateUrl: './match-prediction.html',
  styleUrls: ['./match-prediction.scss']
})
export class MatchPredictionComponent implements OnInit {
  @Input() match!: any;
  prediction?: Prediction;
  isLoading = true;

  constructor(private predictionService: PredictionService) {}

  ngOnInit() {
    if (this.match) {
      this.predictionService.predictMatch(
        this.match.homeTeam,
        this.match.awayTeam
      ).subscribe(prediction => {
        this.prediction = prediction;
        this.isLoading = false;
      });
    }
  }

  getProbabilityWidth(prob: number): string {
    return `${prob * 100}%`;
  }
}