import { Component } from '@angular/core';
import { LiveMatchesComponent } from "./components/live-matches/live-matches";

@Component({
  selector: 'app-root',
  template: `
    <app-live-matches></app-live-matches>
  `,
  styles: [],
  imports: [LiveMatchesComponent]
})
export class AppComponent {}