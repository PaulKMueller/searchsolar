from datetime import date, timedelta

def get_financial_kpis(roof_area, sunlight_hours):
    kpi = dict()

    system_efficiency = 0.15
    electricity_price = 0.30
    average_installation_cost = 10000
    lifetime_panel = 23
    lifetime_panel = 0.3

    annual_savings = roof_area * system_efficiency * sunlight_hours * electricity_price
    break_even_time = average_installation_cost / annual_savings * 365
    roi = (((annual_savings * lifetime_panel) - average_installation_cost) / average_installation_cost ) * 100


    break_even_date = date.today() + timedelta(days=break_even_time)

    kpi['annual_savings'] = annual_savings
    kpi['break_even_date'] = break_even_date
    kpi['roi'] = roi

    return kpi