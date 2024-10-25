from backend.find_geo import find_geo

def orchestrate(plz, city, street, house_number):
    geo = find_geo(plz, city, street, house_number)

    sun_hours = sunshine(geo['latitude'], geo['longitude'])

    kpi = finance(geo['squaremeters'], sun_hours['location'])

    return [geo, sun_hours, kpi]


    