import { Component, OnInit, OnDestroy } from '@angular/core';
import { ModuleService } from 'src/app/services/module.service';
import { ActivatedRoute } from '@angular/router';
import { Module, Setting } from 'src/app/models/module';

@Component({
    selector: 'app-module',
    templateUrl: './module.component.html',
    styleUrls: ['./module.component.scss']
})
export class ModuleComponent implements OnInit, OnDestroy {

    lineChartData: Array<any> = [
        { data: [65, 59, 80, 81, 56, 55, 40], label: 'Series A' },
        { data: [28, 48, 40, 19, 86, 27, 90], label: 'Series B' },
        { data: [18, 48, 77, 9, 100, 27, 40], label: 'Series C' }
    ];
    lineChartLabels: Array<any> = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    lineChartOptions: any = {
        responsive: true
    };

    settings: Setting[];

    constructor(
        public moduleService: ModuleService,

        private route: ActivatedRoute
    ) { }

    ngOnInit() {
    }

    ngOnDestroy() {
        var m = this.module;
        if (m)
            this.moduleService.iDontWantHistory(m);
    }

    get module(): Module {
        var module = this.moduleService.getById(this.route.snapshot.params.id);

        if (!this.settings && module) {
            this.settings = [];
            var sensI = 0;
            for (var sensor of module.sensors) {
                for (var sett of sensor.settings) {
                    var s: Setting = JSON.parse(JSON.stringify(sett));
                    s.sensorI = sensI;
                    this.settings.push(s);
                }
                sensI++;
            }
        }

        if (module)
            this.moduleService.iWantHistory(module);

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

    apply(sett: Setting) {
        this.moduleService.applySetting(this.module, sett);
        sett.changed = false;
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
