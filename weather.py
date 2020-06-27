import requests
import json
import os
import time
from datetime import datetime
def update():
    payload = {'q': 'shanghai,cn', 'appid': '4572df391e878ae8ddcf679c88dba984'}
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=payload)
    weather_dict=r.json()
    export_dict={'forecast':[]}
    for fcast in weather_dict['list'][:12]:
        dt=datetime.fromtimestamp(fcast['dt'])
        real_temp=(fcast['main']['temp']-273.15)
        feels_like=(fcast['main']['feels_like']-273.15)
        pressure_kpa=(fcast['main']['pressure']/10)
        desc=(fcast['weather'][0]['description'])
        # generate url for downloading icon
        icon_url='http://openweathermap.org/img/wn/'+fcast['weather'][0]['icon']+'@4x.png'
        # download icon
        r = requests.get(icon_url, allow_redirects=True)
        icon_path='assets/icons/current_icon_'+dt.strftime('%Y%m%d_%H%M%S')+'.png'
        open(icon_path, 'wb').write(r.content)
        # save to export_dict
        export_dict['forecast'].append({
            'dt':dt.strftime('%Y%m%d_%H%M%S'),
            'real_temp':real_temp,
            'feels_like':feels_like,
            'pressure_kpa':pressure_kpa,
            'desc':desc,
            'icon_url':icon_url,
            'icon_path':icon_path
            })
    
    with open('weather/export.json', 'w') as f:
        f.write(json.dumps(export_dict))
    
    # purge historical icon files
    now = time.time()
    icon_dir='assets/icons/'
    icon_files = [os.path.join(icon_dir, filename) for filename in os.listdir(icon_dir)]
    for f in icon_files:
        if (now - os.stat(f).st_mtime) > 172800: # older than two days
            command = "rm {0}".format(f)
            print(command)
            os.remove(f)

if __name__ == "__main__":
    update()
