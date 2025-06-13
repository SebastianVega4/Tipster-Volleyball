import { Injectable } from '@angular/core';
import { DataService } from './data';
import { Observable, forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';
import { Prediction } from '../models/prediction.model';

@Injectable({ providedIn: 'root' })
export class PredictionService {

  constructor(private dataService: DataService) { }

  predictMatch(homeTeam: string, awayTeam: string): Observable<Prediction> {
    return forkJoin([
      this.dataService.getTeamStats(homeTeam),
      this.dataService.getTeamStats(awayTeam)
    ]).pipe(
      map(([homeStats, awayStats]) => {
        // Lógica de predicción mejorada
        const homeWinRate = homeStats.win_rate || 0.5;
        const awayWinRate = awayStats.win_rate || 0.5;
        
        // Factor de ventaja local
        const homeAdvantage = 0.1;
        
        // Calcular probabilidades
        const homeWinProbability = (homeWinRate * (1 + homeAdvantage)) / 
                                  (homeWinRate * (1 + homeAdvantage) + awayWinRate);
        
        const awayWinProbability = 1 - homeWinProbability;
        
        // Determinar sets esperados
        const setDifference = homeWinRate - awayWinRate;
        let expectedSets = '3-2';
        
        if (setDifference > 0.3) expectedSets = '3-0';
        else if (setDifference > 0.15) expectedSets = '3-1';
        else if (setDifference < -0.3) expectedSets = '0-3';
        else if (setDifference < -0.15) expectedSets = '1-3';
        
        return {
          homeWinProbability,
          awayWinProbability,
          expectedSets,
          keyFactors: [
            { name: 'Ataque', homeValue: homeStats.attack_avg, awayValue: awayStats.attack_avg },
            { name: 'Defensa', homeValue: homeStats.defense_avg, awayValue: awayStats.defense_avg },
            { name: 'Saques', homeValue: homeStats.aces_avg, awayValue: awayStats.aces_avg }
          ]
        };
      })
    );
  }
}

