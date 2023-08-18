import requests
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
import time

def get_satellite_data(norad_id):
    print(obs_latitude)
    response = requests.get(f"https://api.n2yo.com/rest/v1/satellite/positions/{norad_id}/{obs_latitude}/{obs_longitude}/0/2/&apiKey=HQ6AU4-GPGSWK-XK6DQZ-53M0")
    data = response.json()
    info = data.get('info', {})
    positions = data.get('positions', [])
    if positions:
        latest_position = positions[0]
        latitude = float(latest_position['satlatitude'])
        longitude = float(latest_position['satlongitude'])
        altitude = float(latest_position['sataltitude'])
        return latitude, longitude, altitude
    return None, None, None, None

# Karte erstellen
plt.figure(figsize=(10, 8))
m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawparallels(range(-90, 91, 30), labels=[1,0,0,0])
m.drawmeridians(range(-180, 181, 45), labels=[0,0,0,1])
plt.title('Live Satellite Positions')

geolocator = Nominatim(user_agent="satellite_tracker")

plt.ion()  # Aktiviere interaktives Matplotlib-Backend

obs_longitude = 6.98165
obs_latitude = 49.2354

try:
    satellite_data = [
        {'norad_id': 25544, 'color': 'red', 'name': 'ISS'},
        {'norad_id': 20580, 'color': 'blue', 'name': 'Hubble'},
        {'norad_id': 39084, 'color': 'green', 'name': 'Landsat 8'},
        {'norad_id': 39460, 'color': 'purple', 'name': 'Tiangong-2'},
        {'norad_id': 26407, 'color': 'pink', 'name': 'Aqua'},
        {'norad_id': 25994, 'color': 'blue', 'name': 'GOES-12'},
        {'norad_id': 43196, 'color': 'red', 'name': 'GSAT-11'},
        {'norad_id': 37849, 'color': 'purple', 'name': 'WorldView-2'}
    ]
    
    previous_plots = [None] * len(satellite_data)
    
    legend_texts = {}    
    while True:
        for i, satellite in enumerate(satellite_data):
            norad_id = satellite['norad_id']
            latitude, longitude, altitude = get_satellite_data(norad_id)
            
            if latitude is None or longitude is None:
                continue
            
            print(f"Satellite {norad_id}: {latitude}, {longitude}")
            x, y = m(longitude, latitude)
            
            if previous_plots[i]:
                previous_plots[i].remove()
            
            # Zeichne den aktuellen Plot und aktualisiere die Legende
            current_plot = m.plot(x, y, 'o', markersize=10, color=satellite['color'])[0]
            plt.draw()  # Aktualisiere das bestehende Fenster
            
            # Ermittle die Länderinformation
            location = geolocator.reverse((latitude, longitude))
            if location is None:
                country = "Unbekannt"
            else:
                country = location.raw.get('address', {}).get('country', "Unbekannt")


            if i in legend_texts:
                legend_texts[i].remove()

            legend_texts[i] = plt.text(x+2500000, y, f'{satellite["name"]}\nLat: {latitude:.2f}\nLon: {longitude:.2f}',
                                        color=satellite['color'], fontsize=10, ha='center', va='center')            
            # Speichere den aktuellen Plot als vorherigen Plot für die nächste Iteration
            previous_plots[i] = current_plot
        plt.pause(1)  # Warte 1 Sekunde, bevor die nächste Position abgerufen wird


except KeyboardInterrupt:
    print("Programm beendet.")
finally:
    plt.ioff()  # Deaktiviere interaktives Matplotlib-Backend
    plt.show()  # Halte das Fenster geöffnet, nachdem die Schleife beendet wurde
