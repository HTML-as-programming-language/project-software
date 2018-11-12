import { Component, ViewChild, ElementRef, NgZone } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EmWasmComponent } from '../em-wasm.component';

const requestFullscreen =
  document.documentElement.requestFullscreen
  || document.documentElement['webkitRequestFullscreen']
  || document.documentElement['msRequestFullscreen']
  || document.documentElement['mozRequestFullScreen'];

@Component({
  templateUrl: './3d-model.component.html',
  styleUrls: ['./3d-model.component.css']
})
export class Wasm3dCubeComponent extends EmWasmComponent {

  @ViewChild('canvas') canvas: ElementRef;
  error: string;
  supportsFullscreen: boolean;

  constructor(private httpClient: HttpClient, private ngZone: NgZone) {
    super();

    this.supportsFullscreen = !!requestFullscreen;
    this.jsFile = '3d-model.js';
    this.emModule = () => ({
      canvas: <HTMLCanvasElement>this.canvas.nativeElement,
      printErr: (what: string) => {
        if (!what.startsWith('WARNING')) {
          this.ngZone.run(() => this.error = what);
        }
      }
    });
  }

  toggleFullscreen() {
    if (requestFullscreen) {
      requestFullscreen.bind(this.canvas.nativeElement)();
    }
  }
}
