import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MbsComponent } from './components/mbs/mbs.component';

const routes: Routes = [
    {
        path: "", component: MbsComponent
    }
]

@NgModule({
    imports: [ RouterModule.forRoot(routes) ],
    exports: [ RouterModule ]
})
export class AppRoutingModule { }
