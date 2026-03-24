class Airport:
   def __init__(self,ICAO,lat,lon):
       self.ICAO = ICAO
       self.latitude = lat
       self.longitude = lon
       self.schengen = False



EsSc=['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']


def IsSchengenAirport(code):


   Schengen= False
   if code==" ":
       Schengen= False
   else:
       i = 0
       while i<len(EsSc) and not Schengen:
           if code[0:2]==EsSc[i]:
               Schengen= True
           else:
               i=i+1
       return Schengen


def SetSchengen(airport):
    airport.schengen = IsSchengenAirport(airport.ICAO)


def PrintAirport(airport):
    print("ICAO:", airport.ICAO)
    print("Latitude:", airport.latitude)
    print("Longitude:", airport.longitude)
    print("Schengen:", airport.schengen)





def LoadAirports(filename):
   aeroports=[]

   try:
       file=open(filename, "r")
   except FileNotFoundError:
       return aeroports

   file.readline()
   linea=file.readline()


   while linea != "":
       parts= linea.split(" ")


       latitud = parts[1]
       longitud=parts[2]


       graus_lat=float(latitud[1:3])
       minuts_lat=float(latitud[3:5])
       segons_lat=float(latitud[5:7])


       graus_lon=float(longitud[1:3])
       minuts_lon=float(longitud[3:5])
       segons_lon=float(longitud[5:7])


       if latitud[0]=="S":
           graus_lat=graus_lat*(-1)


       if longitud[0]=="W":
           graus_lon=graus_lon*(-1)


       latitud=graus_lat + minuts_lat/60 + segons_lat/3600
       longitud=graus_lon + minuts_lon/60 + segons_lon/3600


       aeroports.append([parts[0],latitud,longitud])
       linea=file.readline()
   return aeroports




def SaveSchengenAirports(airports,filename):
    if len(airports)==0:
        return -1
    try:
        f=open(filename, "w")
        f.write("CODE LAT LON\n")

        siSchengen=False
        i=0
        while i < len(airports):
            A=airports[i]
            if A.schengen==True:
                siSchengen=True
                if A.latitude >=0:
                    lat_dir="N"
                else:
                    lat_dir="S"
                lat_str=lat_dir+str(int(A.latitude))
                if A.longitude >=0:
                    lon_dir="E"
                else:
                    lon_dir="W"
                lon_str=lon_dir+str(int(A.longitude))

                f.write(A.ICAO+" "+lat_str+" "+lon_str+"\n")
            i=i+1
        f.close()
        if siSchengen==True:
            return 0
        else:
            return -1
    except:
        return -1

def AddAirport(airports,airport):
    i=0
    trobat=False
    while i < len(airports) and not trobat:
        if airports[i].ICAO == airport.ICAO:
            trobat=True
        i=i+1
    if trobat:
        return -1
    else:
        airports.append(airport)
        return 0

def RemoveAirport(airports,code):
    i=0
    trobat=False
    while i < len(airports) and not trobat:
        if airports[i].ICAO == code:
            trobat=True
        i=i+1
    if trobat:
        airports.remove(airports[i])
        return 0
    else:
        return -1

import matplotlib.pyplot as plt

def PlotAirports(airports):
    schengen=0
    noschengen=0
    i=0
    while i < len(airports):
        if airports[i].schengen:
            schengen=schengen+1
        else:
            noschengen=noschengen+1
        i=i+1
    plt.bar(["Airports"],[schengen],label="Schengen")
    plt.bar(["Airports"],[noschengen],bottom=[schengen],label="No Schengen")
    plt.ylabel("Number of airports")
    plt.title("Schengen / No Schengen")
    plt.legend()
    plt.show()





