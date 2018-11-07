import { Injectable } from '@angular/core';
import { Module } from '../models/module';
import * as io from 'socket.io-client';

@Injectable({
    providedIn: 'root'
})
export class ModuleService {

    modules: Module[] = [];
    socket: SocketIOClient.Socket;

    constructor() {

        this.socket = (window as any).socket = io.connect("http://localhost:8081");

        const onUpdate = data => {

            console.log(data);
            this.modules = data["modules"];

        };
        this.socket.on("init", onUpdate);
        this.socket.on("update", onUpdate);
    }


}
