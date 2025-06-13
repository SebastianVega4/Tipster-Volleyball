import { Prediction } from "./prediction.model";

export interface Match {
  id: string;
  homeTeam: string;
  awayTeam: string;
  date: string;
  currentSet: number;
  currentScore: string;
  sets: string[];
  status: 'Scheduled' | 'Live' | 'Finished';
  odds: {
    home: number;
    away: number;
  };
  stats: {
    aces: [number, number];
    blocks: [number, number];
    attackEff: [number, number];
  };
  prediction?: Prediction;
}

export interface HistoricalMatch {
  id: string;
  homeTeam: string;
  awayTeam: string;
  date: string;
  result: string;
  sets: string[];
  stats: {
    aces: [number, number];
    blocks: [number, number];
    attackEff: [number, number];
  };
}