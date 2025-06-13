import { Component, Input, OnInit } from '@angular/core';
import { DataService } from '../../services/data';

@Component({
  selector: 'app-team-stats',
  templateUrl: './team-stats.html',
  styleUrls: ['./team-stats.scss']
})
export class TeamStatsComponent implements OnInit {
  @Input() teamName!: string;
  stats: any;
  isLoading = true;

  constructor(private dataService: DataService) {}

  ngOnInit() {
    if (this.teamName) {
      this.dataService.getTeamStats(this.teamName).subscribe(stats => {
        this.stats = stats;
        this.isLoading = false;
      });
    }
  }
}