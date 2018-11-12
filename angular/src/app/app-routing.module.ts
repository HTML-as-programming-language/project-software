import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ModuleComponent } from './components/module/module.component';
import { WasmConsoleLoggerComponent } from "./wasm/example/example.component";

const routes: Routes = [
    { path: "module/:id", component: ModuleComponent },
    { path: 'example', component: WasmConsoleLoggerComponent, data: { demo: true, name: 'Console logger' } },

];

@NgModule({
    imports: [ RouterModule.forRoot(routes) ],
    exports: [ RouterModule ]
})
export class AppRoutingModule { }
