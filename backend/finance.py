from datetime import date, timedelta

def get_financial_kpis(roof_area, sunlight_hours):
    kpi = dict()

    system_efficiency = 0.15
    electricity_price = 0.30
    installation_cost = 70 * roof_area
    lifetime_panel = 23

    annual_savings = roof_area * system_efficiency * sunlight_hours * electricity_price / 8
    break_even_time = installation_cost / annual_savings * 365
    roi = (((annual_savings * lifetime_panel) - installation_cost) / installation_cost ) * 100

    # Convert break_even_time to integer days
    break_even_date = date.today() + timedelta(days=int(break_even_time))

    kpi['annual_savings'] = annual_savings
    kpi['break_even_date'] = break_even_date
    kpi['roi'] = roi

    return kpi

def get_energy_for_hours(roof_area, sunlight_hours):
    print(f"Roof area: {roof_area}")
    print(f"Sunlight hours: {sunlight_hours}")
    
    energy_per_square_meter = 0.16 # in kWp

    energy = roof_area * sunlight_hours * energy_per_square_meter

    return energy
