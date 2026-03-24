

class Aeroports:
    def __init__(self, ICAO, lat, lon):
        self.ICAO = ICAO
        self.latitude = lat
        self.longitude = lon
        self.schengen = False


Airport= open("Airports.txt", "r")
Results=[]
EsSc=['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']


def IsSchengenAirport():
    linea = Airport.readline()
    while linea != "":
        A = Aeroports()
        A.ICAO=linea[0:2]
        i=0
        while i<len(EsSc) and not A.schengen:
            if A.ICAO == EsSc[i]:
                A.schengen = True
            else:
                i=i+1
        Results.append({"Aeroport": A.ICAO, "Schengen": A.schengen})
        linea = Airport.readline()

def SetSchengen(airport):
    airport.schengen = IsSchengenAirport(airport.ICAO)

def PrintAirport(airport):
    print("ICAO:",airport.ICAO)
    print("Latitude:",airport.latitude)
    print("Longitude:",airport.longitude)
    print("Schengen:",airport.schengen)






def LoadAirports(filename):
    airports=[]
    file=open(filename,"r")
    line=file.readline()
    line=file.readline()
    while line!="":
        parts = line.split()
        coordenades = parts[0]
        lat_str = parts[1]
        lon_str = parts[2]

        if lat_str[0]=="N" or lat_str[0]=="S":
            lat_graus = float(lat_str[1:3])
            lat_minuts = float(lat_str[3:5])
            lat_sec = float(lat_str[5:7])
            lat_final = lat_graus + (lat_minuts / 60) + (lat_sec / 3600)
            if lat_str[0] == "S":
                lat_final = -lat_final
        if lon_str[0]=="W" or lon_str[0]=="E":
            lon_graus = float(lon_str[1:4])
            lon_minuts = float(lon_str[4:6])
            lon_sec = float(lon_str[6:8])
            lon_final = lon_graus + (lon_minuts / 60) + (lon_sec / 3600)
            if lon_str[0] == "W":
                lon_final = -lon_final
        airport=Airport(coordenades,lat_final,lon_final)
        airports.append(airport)

        line=file.readline()
    file.close()
    return airports

def SaveSchengenAirports(airports,filename):
    if len(airports)==0:
        return -1
    file=open(filename,"w")
    file.write("CODE LAT LON\n")
    i=0
    written=0
    while i<len(airports):
        if airports[i].schengen==True:
            lat=airports[i].latitude
            lon=airports[i].longitude
            if lat>=0:
                lat_dir="N"
            else:
                lat_dir="S"
                lat=-lat
            if lon>=0:
                lon_dir="E"
            else:
                lon_dir="W"
                lon=-lon

            lat_deg=float(lat)
            lat_min_total=(lat-lat_deg)*60
            lat_min=float(lat_min_total)
            lat_sec=float((lat_min_total - lat_min)*60)

            lon_deg = float(lon)
            lon_min_total = (lon - lon_deg) * 60
            lon_min = float(lon_min_total)
            lon_sec = float((lon_min_total - lon_min) * 60)

            lat_str=lat_dir+str(lat_deg).zfill(2)+str(lat_min).zfill(2)+str(lat_sec).zfill(2)
            lon_str=lon_dir+str(lon_deg).zfill(2)+str(lon_min).zfill(2)+str(lon_sec).zfill(2)

            file.write(airports[i].ICAO + " " + lat_str + " " +
                       lon_str + "\n")
            written = written + 1

        i = i + 1

        file.close()

        if written == 0:
            return -1
        else:
            return 0

def AddAirport(airports, airport):
    i = 0
    found = False

    while i < len(airports) and not found:
        if airports[i].ICAO == airport.ICAO:
            found = True
        i = i + 1

    if not found:
        airports.append(airport)

def RemoveAirport(airports, code):
    i = 0
    found = False

    while i < len(airports) and not found:
        if airports[i].ICAO == code:
            found = True
        else:
            i = i + 1

    if found:
        airports.pop(i)
        return 0
    else:
        return -1

import matplotlib.pyplot as plt

def PlotAirports(airports):
    schengen = 0
    no_schengen = 0

    i = 0
    while i < len(airports):
        if airports[i].schengen:
            schengen = schengen + 1
        else:
            no_schengen = no_schengen + 1
        i = i + 1

    plt.bar(["Airports"], [schengen], label="Schengen")
    plt.bar(["Airports"], [no_schengen], bottom=[schengen],
            label="No Schengen")
    plt.ylabel("Number of airports")
    plt.title("Schengen / No Schengen airports")
    plt.legend()
    plt.show()

def MapAirports(airports):
    file = open("airports.kml", "w")

    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    file.write('<Document>\n')

    i = 0
    while i < len(airports):
        file.write('<Placemark>\n')
        file.write('<name>' + airports[i].ICAO + '</name>\n')

        if airports[i].isSchengen == True:
            file.write('<Style>\n')
            file.write('<IconStyle>\n')
            file.write('<color>ff00ff00</color>\n')
            file.write('</IconStyle>\n')
            file.write('</Style>\n')
        else:
            file.write('<Style>\n')
            file.write('<IconStyle>\n')
            file.write('<color>ff0000ff</color>\n')
            file.write('</IconStyle>\n')
            file.write('</Style>\n')

        file.write('<Point>\n')
        file.write(
            '<coordinates>' + str(airports[i].longitude) + ',' +
            str(airports[i].latitude) + ',0</coordinates>\n')
        file.write('</Point>\n')
        file.write('</Placemark>\n')

        i = i + 1

    file.write('</Document>\n')
    file.write('</kml>\n')

    file.close()