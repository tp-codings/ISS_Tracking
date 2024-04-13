import requests
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
import keyboard
import sys

geolocator = Nominatim(user_agent="iss_tracker")

def get_iss_data():
    response = requests.get("http://api.wheretheiss.at/v1/satellites/25544")
    data = response.json()
    longitude = data['longitude']
    latitude = data['latitude']
    velocity = data['velocity']  
    altitude = data['altitude']  
    return longitude, latitude, velocity, altitude

plt.figure(figsize=(10, 8))
m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawparallels(range(-90, 91, 30), labels=[1,0,0,0])
m.drawmeridians(range(-180, 181, 45), labels=[0,0,0,1])
plt.title('Live Position of ISS')

stop = False
previous_plot = None  
first_iteration = True 

while not stop:
    longitude, latitude, velocity, altitude = get_iss_data()
    print(latitude, longitude)
    x, y = m(longitude, latitude)
    
    if previous_plot:
        previous_plot.remove()
    
    try:
        location = geolocator.reverse((latitude, longitude), timeout=10)
        country = location.raw['address']['country']
        print(country)
        country = country.encode('utf-8').decode('utf-8')
        print(country)
    except Exception as e:
        print("Fehler bei der Länderermittlung:", str(e))
        country = "Somewhere over the ocean"
    
    current_plot = m.plot(x, y, 'ro', markersize=10)[0]
    plt.draw()  
    
    if first_iteration:
        legend = plt.legend([f'ISS Current Position ({country})\n'
                                f'Velocity: {velocity:.2f} km/h\n'
                                f'Altitude: {altitude:.2f} km'])
        first_iteration = False
    else:
        legend.get_texts()[0].set_text(f'ISS Current Position ({country})\n'
                                        f'Velocity: {velocity:.2f} km/h\n'
                                        f'Altitude: {altitude:.2f} km')
    
    previous_plot = current_plot
    if keyboard.is_pressed("q"):
        stop = True
        sys.exit()
        break

    plt.pause(1)  