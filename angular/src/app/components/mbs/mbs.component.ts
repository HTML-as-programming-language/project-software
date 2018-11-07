import { Component, OnInit } from '@angular/core';
import { ModuleService } from 'src/app/services/module.service';

@Component({
    selector: 'app-mbs',
    templateUrl: './mbs.component.html',
    styleUrls: ['./mbs.component.scss']
})
export class MbsComponent implements OnInit {

    constructor(
        public moduleService: ModuleService
    ) { }

    ngOnInit() {
    }

}
