import { Component, OnInit } from '@angular/core';
import { ModuleService } from 'src/app/services/module.service';
import { ActivatedRoute } from '@angular/router';
import { Module, Setting } from 'src/app/models/module';

@Component({
    selector: 'app-module',
    templateUrl: './module.component.html',
    styleUrls: ['./module.component.scss']
})
export class ModuleComponent implements OnInit {

    settings: Setting[];

    constructor(
        public moduleService: ModuleService,

        private route: ActivatedRoute
    ) { }

    ngOnInit() {
    }

    get module(): Module {
        var module = this.moduleService.getById(this.route.snapshot.params.id);

        if (!this.settings && module) {
            this.settings = [];
            for (var sensor of module.sensors)
                for (var sett of sensor.settings)
                        this.settings.push(JSON.parse(JSON.stringify(sett)));
        }

        return module;
    }

    get data() {
        var m = this.module;
        if (!m) return;
        var data = [];
        const getData = (obj, startWithLabel) => {
            if (!obj) return;
            for (var key in obj) 
                if (typeof key == "string" && (!startWithLabel || key.startsWith("label"))) 
                    data.push([startWithLabel ? key.substr(5) : key, obj[key]]);
        }
        getData(m.data, true);
        for (var sensor of m.sensors) getData(sensor.data, false);
        return data;
    }

    minRange(sett: Setting): number {
        if (sett.id == "temp_threshold")
            return -30;
        return 0;
    }

    maxRange(sett: Setting): number {
        if (sett.id == "temp_threshold")
            return 50;
        return 100;
    }

}
