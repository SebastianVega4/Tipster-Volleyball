import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Match, HistoricalMatch } from '../models/match.model';
import { Team } from '../models/team.model';

@Injectable({ providedIn: 'root' })
export class DataService {
  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  getTeams(): Observable<Team[]> {
    return this.http.get<Team[]>(`${this.apiUrl}/teams`);
  }

  getMatches(): Observable<Match[]> {
    return this.http.get<Match[]>(`${this.apiUrl}/matches`);
  }

  getLiveMatches(): Observable<Match[]> {
    return this.http.get<Match[]>(`${this.apiUrl}/matches/live`);
  }

  getTeamStats(teamName: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/team-stats/${teamName}`);
  }

  getHistoricalMatches(): Observable<HistoricalMatch[]> {
    return this.http.get<HistoricalMatch[]>(`${this.apiUrl}/historical-matches`);
  }
}