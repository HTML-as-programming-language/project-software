import { Injectable } from '@angular/core';
import { Module, Setting } from '../models/module';
import * as io from 'socket.io-client';
import { UtilsService } from './utils.service';

@Injectable({
    providedIn: 'root'
})
export class ModuleService {

    modules: Module[] = [];
    socket: SocketIOClient.Socket;

    history: Array<any> = [
        { data: [], label: 'bla' }
    ];
    historyLabels: Array<any> = [];

    constructor(
        private utils: UtilsService
    ) {

        this.socket = (window as any).socket = io.connect("http://localhost:8081");

        const onUpdate = data => {this.modules = data["modules"]; console.log(data)};
        this.socket.on("init", onUpdate);
        this.socket.on("update", onUpdate);

        this.socket.on("historyInit", data => {
            var his = []
            for (var i = 1; i < data.names.length; i++) {
                his.push({
                    data: data.data.map(arr => arr[i]),
                    label: data.names[i]
                })
                this.historyLabels = data.data.map(arr => utils.timestampToString(arr[0], true))
            }
            this.history = his;
        });
        this.socket.on("historyUpdate", data => {

            var his = this.history;
            for (var i = 1; i < data.length; i++) {
                if (i - 1 in his)
                    his[i - 1].data.push(data[i])
            }
            this.history = his;
            this.historyLabels = this.historyLabels.concat([utils.timestampToString(data[0], true)])

        });
    }

    getById(id: string): Module {
        for (var m of this.modules) if (m.id == id) return m;
    }

    applySetting(module: Module, sett: Setting) {
        var body;

        switch (sett.subtype) {
            case "minmax":
                body = `[${sett.min}, ${sett.max}]`;
                break;
            default:
                return;
        }
        var path = sett.sensorSetting ? 
        `module/${module.id}/sensor/${sett.sensorI}/${sett.id}`
        :
        `module/${module.id}/setting/${sett.id}`

        console.log(body)
        this.socket.emit("request", {
            path,
            body
        });
    }

    toggleHatch(module: Module, open) {
        this.socket.emit("request", {
            path: `module/${module.id}/setting/hatch_force`,
            body: open ? 1 : 0
        });
    }

    iWantHistory(module: Module) {
        this.socket.emit("iWantHistory", module.id);
    }

    iDontWantHistory(module: Module) {
        this.socket.emit("iDoNotWantHistory", module.id);
    }

    toggleAutomatic(module: Module, automatic) {
        this.socket.emit("request", {
            path: `module/${module.id}/setting/automatic`,
            body: automatic ? 1 : 0
        });
    }

}
