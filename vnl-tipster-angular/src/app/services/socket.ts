import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable } from 'rxjs';
import { Match } from '../models/match.model';

@Injectable({ providedIn: 'root' })
export class SocketService {
  constructor(private socket: Socket) {}

  getLiveMatches(): Observable<Match[]> {
    return this.socket.fromEvent('live_matches');
  }

  getMatchUpdates(): Observable<{ match_id: string; data: Match }> {
    return this.socket.fromEvent('match_update');
  }

  subscribeToMatch(matchId: string): void {
    this.socket.emit('subscribe_match', matchId);
  }
}