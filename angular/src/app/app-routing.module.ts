import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ModuleComponent } from './components/module/module.component';
import { WasmConsoleLoggerComponent } from "./wasm/example/example.component";
import { Wasm3dCubeComponent } from "./wasm/3d-model/3d-model.component";

const routes: Routes = [
    { path: "module/:id", component: ModuleComponent },
    { path: 'example', component: WasmConsoleLoggerComponent, data: { demo: true, name: 'Console logger' } },
    { path: '3d-model', component: Wasm3dCubeComponent, data: { demo: true, name: '3D model' } },

];

@NgModule({
    imports: [ RouterModule.forRoot(routes) ],
    exports: [ RouterModule ]
})
export class AppRoutingModule { }
