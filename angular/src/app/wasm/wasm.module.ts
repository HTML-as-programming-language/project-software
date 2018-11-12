import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { LaddaModule } from 'angular2-ladda';

import { Wasm3dCubeComponent } from "./3d-model/3d-model.component";
import { WasmConsoleLoggerComponent } from "./example/example.component";

@NgModule({
  declarations: [
    WasmConsoleLoggerComponent,
    Wasm3dCubeComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    LaddaModule.forRoot({
      style: 'zoom-in',
      spinnerSize: 30,
    })
  ]
})
export class WasmModule { }
