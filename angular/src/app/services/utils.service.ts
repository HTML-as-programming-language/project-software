import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class UtilsService {

    constructor() { }

    /**
     * timestamp to string
     * 
     * @param timestamp
     * @param onlyTime like '13:40'
     */
    timestampToString(timestamp: number, onlyTime: boolean): string {
        var a = new Date(timestamp > 1000000000000 ? timestamp : timestamp * 1000);
        var b = new Date();

        var year = a.getFullYear();
        var month = a.getMonth();
        var date = a.getDate();
        var hour = a.getHours();
        var min: any = a.getMinutes();
        var string = '';
        var minStr = min < 10 ? "0" + min : min;

        if (onlyTime) return hour + ":" + minStr;

        var months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];

        if (year == b.getFullYear()) {
            if (date != b.getDate() || month != b.getMonth()) {
                if (month == b.getMonth() && b.getDate() - date == 1) {
                    string += 'Yesterday ';
                } else {
                    string += date + ' ' + months[month] + ' ';
                }
            }
        } else {
            string += date + ' ' + months[month] + ' ' + year + ' ';
        }

        string += 'at ' + hour + ':' + minStr;
        return string;
    }

}
