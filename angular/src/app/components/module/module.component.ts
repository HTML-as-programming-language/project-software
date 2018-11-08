import { Component, OnInit } from '@angular/core';
import { ModuleService } from 'src/app/services/module.service';
import { ActivatedRoute } from '@angular/router';
import { Module } from 'src/app/models/module';

@Component({
    selector: 'app-module',
    templateUrl: './module.component.html',
    styleUrls: ['./module.component.scss']
})
export class ModuleComponent implements OnInit {

    constructor(
        public moduleService: ModuleService,

        private route: ActivatedRoute
    ) { }

    ngOnInit() {
    }

    get module(): Module {
        return this.moduleService.getById(this.route.snapshot.params.id);
    }

    get data() {
        var m = this.module;
        if (!m) return;
        var data = [];
        for (var key in m.data) 
            if (typeof key == "string" && key.startsWith("label")) 
                data.push([key.substr(5), m.data[key]]);
        return data;
    }

}
