import json
from pprint import pprint

if __name__ == '__main__':
    data_str = '{"modules":[{"data":{"automatic":"True","distance":0,"hatch_status":100,"labelAutomatic":"True","labelDistance":"0cm","labelHatch open":"100%"},"id":"devttyACM0","label":"/dev/ttyACM0","sensors":[{"data":{"label":"2.6C","temp":2.6},"id":"0","label":"Temperature","settings":[{"id":"temp_threshold","label":"Temperature thresholds","max":30,"min":0,"subtype":"minmax","type":"int"}],"type":"TEMP"},{"data":{"label":"36%","light":36},"id":"1","label":"Light","settings":[{"id":"light_threshold","label":"Light thresholds","max":100,"min":0,"subtype":"minmax","type":"int"}],"type":"LIGHT"}]}]}'

    # print(data_str.replace("'", '"'))
    data = json.loads(data_str)
    new_data = []
    for sensor in data["modules"][0]["sensors"]:
        # pprint(list(sensor["data"].values())[1])
        new_data.append(list(sensor["data"].values())[1])

