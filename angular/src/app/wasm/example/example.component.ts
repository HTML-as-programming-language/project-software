import { Component, NgZone } from '@angular/core';
import { EmWasmComponent } from '../em-wasm.component';

@Component({
  templateUrl: './example.component.html'
})
export class WasmConsoleLoggerComponent extends EmWasmComponent {

  logItems: string[] = [];

  constructor(ngZone: NgZone) {
    super();

    this.jsFile = 'example.js';
    this.emModule = () => ({
      print: what => {
        ngZone.run(() => this.logItems.push(what));
      }
    });
  }
}
