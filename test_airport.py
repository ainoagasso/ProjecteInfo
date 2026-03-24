from airport import *
airport = Airport ("LEBL", 41.297445, 2.0832941)
airports=open("Airports.txt","r")
SetSchengen(airport)
PrintAirport (airport)


class Airport:
    def __init__(self, ICAO, latitude, longitude, schengen=False):
        self.ICAO = ICAO
        self.latitude = latitude
        self.longitude = longitude
        self.schengen = schengen










