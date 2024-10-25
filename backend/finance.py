def get_financial_kpis(roof_area, sunlight_hours):
    kpi = dict()

    system_efficiency = 0.15
    electricity_price = 0.30
    average_installation_cost = 10000
    lifetime_panel = 23

    annual_savings = roof_area * system_efficiency * sunlight_hours * electricity_price
    break_even = average_installation_cost / annual_savings
    roi = (((annual_savings * lifetime_panel) - average_installation_cost) / average_installation_cost ) * 100

    kpi['annual_savings'] = annual_savings
    kpi['break_even_after'] = break_even
    kpi['roi'] = roi

    return kpi