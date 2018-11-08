import { Component, OnInit } from '@angular/core';
import { ModuleService } from 'src/app/services/module.service';

@Component({
    selector: 'app-modules-list',
    templateUrl: './modules-list.component.html',
    styleUrls: ['./modules-list.component.scss']
})
export class ModulesListComponent implements OnInit {

    constructor(
        public modulesService: ModuleService
    ) { }

    ngOnInit() {
    }

}
