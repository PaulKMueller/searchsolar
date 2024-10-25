from backend.find_geo import find_geo
from backend.sunshine import get_sunshine_hours
from backend.finance import calculate_finance

def orchestrate(plz, city, street, house_number):
    geo = find_geo(plz, city, street, house_number)

    sun_hours = sunshine(geo['latitude'], geo['longitude'])

    kpi = finance(geo['squaremeters'], sun_hours['location'])

    return [geo, sun_hours, kpi]


    