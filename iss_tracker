import requests
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="iss_tracker")

def get_iss_data():
    response = requests.get("http://api.wheretheiss.at/v1/satellites/25544")
    data = response.json()
    longitude = data['longitude']
    latitude = data['latitude']
    velocity = data['velocity']  # Geschwindigkeit in km/h
    altitude = data['altitude']  # Höhe in km
    return longitude, latitude, velocity, altitude

# Karte erstellen
plt.figure(figsize=(10, 8))
m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawparallels(range(-90, 91, 30), labels=[1,0,0,0])
m.drawmeridians(range(-180, 181, 45), labels=[0,0,0,1])
plt.title('Live Position of ISS')

plt.ion()  # Aktiviere interaktives Matplotlib-Backend

try:
    previous_plot = None  # Variable zur Aufbewahrung des vorherigen Plots
    first_iteration = True  # Variable für die erste Iteration
    while True:
        longitude, latitude, velocity, altitude = get_iss_data()
        print(latitude, longitude)
        x, y = m(longitude, latitude)
        
        # Lösche den vorherigen Plot, falls vorhanden
        if previous_plot:
            previous_plot.remove()
        
        try:
            # Ermittle die Länderinformation
            location = geolocator.reverse((latitude, longitude), timeout=10)
            country = location.raw['address']['country']
            print(country)
            country = country.encode('utf-8').decode('utf-8')
            print(country)
        except Exception as e:
            print("Fehler bei der Länderermittlung:", str(e))
            country = "Somewhere over the ocean"
        
        # Zeichne den aktuellen Plot und füge die Informationen zur Legende hinzu
        current_plot = m.plot(x, y, 'ro', markersize=10)[0]
        plt.draw()  # Aktualisiere das bestehende Fenster
        
        # Bei der ersten Iteration, initialisiere die Legende und setze den Text
        if first_iteration:
            legend = plt.legend([f'ISS Current Position ({country})\n'
                                 f'Velocity: {velocity:.2f} km/h\n'
                                 f'Altitude: {altitude:.2f} km'])
            first_iteration = False
        else:
            # Aktualisiere den Text in der Legende
            legend.get_texts()[0].set_text(f'ISS Current Position ({country})\n'
                                           f'Velocity: {velocity:.2f} km/h\n'
                                           f'Altitude: {altitude:.2f} km')
        
        plt.pause(1)  # Warte 1 Sekunde, bevor die nächste Position abgerufen wird
        
        # Speichere den aktuellen Plot als vorherigen Plot für die nächste Iteration
        previous_plot = current_plot

except KeyboardInterrupt:
    print("Programm beendet.")
finally:
    plt.ioff()  # Deaktiviere interaktives Matplotlib-Backend
    plt.show()  # Halte das Fenster geöffnet, nachdem die Schleife beendet wurde
