import { Injectable } from '@angular/core';
import { Module, Setting } from '../models/module';
import * as io from 'socket.io-client';

@Injectable({
    providedIn: 'root'
})
export class ModuleService {

    modules: Module[] = [];
    socket: SocketIOClient.Socket;

    constructor() {

        this.socket = (window as any).socket = io.connect("http://localhost:8081");

        const onUpdate = data => this.modules = data["modules"];
        this.socket.on("init", onUpdate);
        this.socket.on("update", onUpdate);

        this.socket.on("historyInit", data => {

        });
        this.socket.on("historyUpdate", data => {

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

        this.socket.emit("request", {
            path: `module/${module.id}/sensor/${sett.sensorI}/${sett.id}/`,
            body
        });
    }

    openHatch(module: Module) {
        
    }

    closeHatch(module: Module) {
        
    }

    iWantHistory(module: Module) {
        this.socket.emit("iWantHistory", module.id);
    }

    iDontWantHistory(module: Module) {
        this.socket.emit("iDoNotWantHistory", module.id);
    }

}
