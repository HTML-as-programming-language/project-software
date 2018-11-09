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

    lineChartOptions: any = {
        responsive: true,
        animation: false,
        elements: { point: { radius: 0 } }
    };

    _module: Module;
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

        if (module && !this._module) {
            this.moduleService.iWantHistory(module);
            this._module = module;
        }

        return module;
    }

    get data() {
        var m = this.module;
        if (!m) return;
        var data = [];

        for (var key in m.data) {
            if (typeof key == "string" && key.startsWith("label"))
                data.push([key.substr(5), m.data[key]]);
        }
        for (var sensor of m.sensors)
            data.push([sensor.label, sensor.data["label"]])

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
