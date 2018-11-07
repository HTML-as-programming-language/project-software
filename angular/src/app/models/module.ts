const example = {
    "modules": [
        {
            "data": { "hatch_status": 8, "labelHatch open": "8%" },
            "id": "devttyACM0",
            "label": "/dev/ttyACM0",
            "sensors": [{
                "data": { "label": "16C", "temp": 16 },
                "id": "0",
                "label": "Temperature",
                "settings": [
                    {
                        "id": "temp_threshold",
                        "label": "Temperature thresholds",
                        "max": 30,
                        "min": 0,
                        "subtype": "minmax",
                        "type": "int"
                    }
                ],
                "type": "TEMP"
            }]
        }
    ]
}


export interface Module {

    id: string,
    label: string,
    sensors: Sensor[],


}

export interface Sensor {

    data?,
    id: string,
    label: string,
    settings: Setting[],
    type: string

}

export interface Setting {

    id: string,
    label: string,
    type: string,
    subtype?: string,
    min?: number,
    max?: number

}
