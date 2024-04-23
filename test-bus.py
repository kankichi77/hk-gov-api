from bus import *

if __name__ == "__main__":
    route_number = "789"
    user_input = input("Input Bus Route Number [default: 789]: ")
    if user_input: route_number = user_input
    APImanager = HKBUSAPI_Manager()
    route = APImanager.getBusRoute(route_number)
    print(f"{route.route}: FROM {route.orig_en} TO {route.dest_en}")
    print(f"Stops on this route: {APImanager.getRouteStopsList(route_number, 'inbound')}")
    user_input = input("Input bus stop number: ")
    if user_input:
        busstop = APImanager.getBusStop(user_input)
        print(f"{busstop.stop}: {busstop.name_en}")