export interface Prediction {
  homeWinProbability: number;
  awayWinProbability: number;
  expectedSets: string;
  keyFactors: {
    name: string;
    homeValue: number;
    awayValue: number;
  }[];
}