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

        setInterval(() => {

            if ('speechSynthesis' in window && this.modulesService.modules.length == 0) {
                var msg = new SpeechSynthesisUtterance();
                var voices = window.speechSynthesis.getVoices();
                if (voices.length > 0) {
                    console.log("Your browser supports " + voices.length + " voices");
                    console.log(voices);
                    msg.voice = voices.filter(function (voice) { return voice.lang == "nl"; })[1];
                }
                msg["voiceURI"] = 'native';
                msg.volume = 1; // 0 to 1
                msg.rate = 0.8; // 0.1 to 10
                msg.pitch = 1; //0 to 2
                msg.text = "Sluit uw module aan a.u.b.";
                msg.lang = "nl";
                speechSynthesis.speak(msg);
            }

        }, 10000);

    }

}
