import urllib.request as request
from dataclasses import dataclass
import json

@dataclass
class ETA():
    co: str
    route: str
    dir: str
    seq: str
    stop: str
    dest_tc: str
    dest_en: str
    eta: str
    rmk_tc: str
    eta_seq: str
    dest_sc: str
    rmk_en: str
    rmk_sc: str
    data_timestamp: str

@dataclass
class RouteStop():
    co: str
    route: str
    dir: str
    seq: str
    stop: str
    data_timestamp: str

    @classmethod
    def initFromJson(cls, json: json):
        return cls(
            co = json["co"],
            route = json["route"],
            dir = json["dir"],
            seq = json["seq"],
            stop = json["stop"],
            data_timestamp = json["data_timestamp"],
        )
    
@dataclass
class BusStop():
    stop: str
    name_tc: str
    name_en: str
    lat: str
    long: str
    name_sc: str
    data_timestamp: str

    @classmethod
    def initFromJson(cls, json: json):
        return cls(
            stop = json["stop"],
            name_tc = json["name_tc"],
            name_en = json["name_en"],
            lat = json["lat"],
            long = json["long"],
            name_sc = json["name_sc"],
            data_timestamp = json["data_timestamp"],
        )
    
@dataclass
class Route():
    co: str
    route: str
    orig_tc: str
    orig_en: str
    dest_tc: str
    dest_en: str
    orig_sc: str
    dest_sc: str
    data_timestamp: str

    @classmethod
    def initFromJson(cls, json: json):
        return cls(
            co = json["co"],
            route = json["route"],
            orig_tc = json["orig_tc"],
            orig_en = json["orig_en"],
            dest_tc = json["dest_tc"],
            dest_en = json["dest_en"],
            orig_sc = json["orig_sc"],
            dest_sc = json["dest_sc"],
            data_timestamp = json["data_timestamp"],
        )


class HKBUSAPI_Manager():
    RoutesList: list[Route] = None
    RouteStopsList : list[RouteStop] = None

    def initRouteStops(self, routenumber, dir) -> list[RouteStop]:
        if self.RouteStopsList: return self.RouteStopsList
        url = "https://rt.data.gov.hk/v2/transport/citybus/route-stop/ctb/"
        url += routenumber + "/" + dir
        with request.urlopen(url) as response:
            api_output = json.loads(response.read().decode('utf8'))
        routestopList = []
        for routestop in api_output["data"]:
            routestopList.append(RouteStop.initFromJson(routestop))
        self.RouteStopsList = routestopList
        return routestopList

    def getRouteStopsList(self, routenumber, dir) -> list:
        self.initRouteStops(routenumber, dir)
        output = []
        for rs in self.RouteStopsList:
            output.append(rs.stop)
        return output

    def getRouteStop(self, routenumber, dir, stop):
        self.initRouteStops(routenumber, dir)
        for rs in self.RouteStopsList:
            if stop == rs.stop:
                return rs
        return None
    
    def initBusRoutes(self) -> list[Route]:
        if self.RoutesList: return self.RoutesList
        url = "https://rt.data.gov.hk/v2/transport/citybus/route/ctb"
        with request.urlopen(url) as response:
            api_output = json.loads(response.read().decode('utf8'))
        routeList = []
        for route in api_output["data"]:
            routeList.append(Route.initFromJson(route))
        self.RoutesList = routeList
        return routeList
    
    # def getBusRouteNumbersList(self) -> list:
    #     self.initBusRoutes()
    #     output = []
    #     for r in self.RoutesList:
    #         output.append(r.route)
    #     return output

    def getBusRoute(self, route):
        self.initBusRoutes()
        for r in self.RoutesList:
            if route == r.route:
                return r
        return None
    
    def getBusStop(self, stopnumber) -> BusStop:
        url = "https://rt.data.gov.hk/v2/transport/citybus/stop/"
        url += stopnumber
        with request.urlopen(url) as response:
            api_output = json.loads(response.read().decode('utf8'))
        return BusStop.initFromJson(api_output["data"])