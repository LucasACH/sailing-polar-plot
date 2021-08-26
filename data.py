from numpy import radians,cos,sin,arctan2

class Data:

    def __init__(
            self,
            lats,
            longs,
            vels,
            wind_direction: float=0,
            max_speed: float=float('inf'),
            min_speed: float=0,
            starboard_tack_max_angle: int=145,
            starboard_tack_min_angle: int=30,
            port_tack_max_angle: int=330,
            port_tack_min_angle: int=205
        ):

        self.lats = lats
        self.longs = longs
        self.vels = vels
        self.wind_direction = wind_direction
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.starboard_tack_max_angle = starboard_tack_max_angle
        self.starboard_tack_min_angle = starboard_tack_min_angle
        self.port_tack_max_angle = port_tack_max_angle
        self.port_tack_min_angle = port_tack_min_angle
        self.coordinates = self.parseCoordinates()


    def parseCoordinates(self):
        '''
        Creates data sets for the latitudinal and longitudinal coordinates.

        Returns
        -------
            [{'lat': a: float, 'lon': b: float}, ... ] | ∀ a,b∈R
        '''

        coordinates = []

        for i in range(len(self.lats) - 1):

            lat_a = float(self.lats[i].firstChild.nodeValue)
            lon_a = float(self.longs[i].firstChild.nodeValue)

            lat_b = float(self.lats[i + 1].firstChild.nodeValue)
            lon_b = float(self.longs[i + 1].firstChild.nodeValue)

            coordinates.append(
                [
                    {'lat': radians(lat_a), 'lon': radians(lon_a)},
                    {'lat': radians(lat_b), 'lon': radians(lon_b)}
                ]
            )

        return coordinates


    def parseBearings(self):
        '''
        Creates a list of bearings.

        Returns
        -------
            [n: float, ... ] | 0 <= n: float <= radians(360)
        '''

        bearings = []

        for coord in self.coordinates:
            bearings.append(self.calculateBearing(coord[0], coord[1]))
        
        return bearings


    def calculateBearing(
        self,
        a: dict={'lat': 0, 'lon': 0},
        b: dict={'lat': 0, 'lon': 0}
        ):
        '''
        Calculates angle *(radians)* between two coordinates.

        Parameters
        ----------
            a: dict, first coordinate data set.
            b: dict, second coordinate data set.

        Returns
        -------
            0 <= n: float <= radians(360)
        '''

        dL = b['lon'] - a['lon']

        X = cos(b['lat']) * sin(dL)
        Y = cos(a['lat']) * sin(b['lat']) - sin(a['lat']) * cos(b['lat']) * cos(dL)

        bearing = arctan2(X,Y)
        bearing = (bearing + radians(360) - radians(self.wind_direction)) % radians(360)
        
        return bearing


    def parseSpeeds(self):
        '''
        Creates a list of speeds.

        Returns
        -------
            [n: float, ... ] | ∀ n∈N
        '''

        speeds = []

        for i in range(len(self.vels) - 1):

            speed = float(self.vels[i].firstChild.nodeValue)
            speeds.append(speed * 1.943844)
        
        return speeds
    

    def maxSpeed(self):
        return round(max(self.parseSpeeds()), 2)


    def averageSpeed(self):
        speeds = self.parseSpeeds()
        average_speed = round(sum(speeds) / len(speeds), 2)
        return average_speed


    def mergeDataSets(self):
        '''
        Combines bearing and speed data sets.

        Returns
        -------
            {
            'theta_max': [n: float, ... ],
            'r_max': [n: float, ... ],
            'theta_avg': [n: float, ... ],
            'r_avg': [n: float, ... ]
            }
        '''
        
        bearings = self.parseBearings()
        speeds = self.parseSpeeds()

        dataSet = {}

        for i in range(len(bearings)):
            bearing = round(bearings[i], 1)
            speed = speeds[i]

            if (
                (bearing >= radians(self.starboard_tack_min_angle) and
                bearing <= radians(self.starboard_tack_max_angle)) or
                (bearing >= radians(self.port_tack_min_angle) and
                bearing <= radians(self.port_tack_max_angle))
            ):
                try:
                    dataSet[bearing].append(speed)
                except KeyError:
                    dataSet[bearing] = [speed]
            
            else:
                dataSet[bearing] = [0]

    
        filteredDataSet = {}

        for theta, r in dataSet.items():
            filteredRadius = [0]

            for value in r:
                if (value >= self.min_speed and value <= self.max_speed):
                    filteredRadius.append(value)
            
            filteredDataSet[theta] = filteredRadius
        
        sortedDataSet = {
            'theta_max': [],
            'r_max': [],
            'theta_avg': [],
            'r_avg': []
            }

        for item in sorted(filteredDataSet.items()):
            sortedDataSet['theta_max'].append(item[0])
            sortedDataSet['r_max'].append(max(item[1]))

            sortedDataSet['theta_avg'].append(item[0])
            sortedDataSet['r_avg'].append(sum(item[1]) / len(item[1]))     
        
        return sortedDataSet


