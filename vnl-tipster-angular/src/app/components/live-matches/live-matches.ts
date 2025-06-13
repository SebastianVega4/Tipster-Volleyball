import { Component, OnInit, OnDestroy } from '@angular/core';
import { SocketService } from '../../services/socket';
import { DataService } from '../../services/data';
import { Match } from '../../models/match.model';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-live-matches',
  templateUrl: './live-matches.html',
  styleUrls: ['./live-matches.scss']
})
export class LiveMatchesComponent implements OnInit, OnDestroy {
  matches: Match[] = [];
  private subscriptions = new Subscription();

  constructor(
    private socketService: SocketService,
    private dataService: DataService
  ) {}

  ngOnInit() {
    // Cargar partidos iniciales
    this.dataService.getLiveMatches().subscribe(matches => {
      this.matches = matches;
    });

    // Escuchar actualizaciones en tiempo real
    const updateSub = this.socketService.getMatchUpdates().subscribe(update => {
      const index = this.matches.findIndex(m => m.id === update.match_id);
      
      if (index !== -1) {
        this.matches[index] = update.data;
      } else {
        // Si es un nuevo partido en vivo
        this.matches.push(update.data);
      }
    });
    
    this.subscriptions.add(updateSub);
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  getProgressWidth(odd: number): string {
    return `${odd * 100}%`;
  }
}