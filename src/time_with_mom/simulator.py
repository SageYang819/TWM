import numpy as np

def simulate(
    n_sim,
    mom_age,
    life_mean,
    life_std,
    abroad_years,
    visits_per_year,
    days_per_visit,
    domestic_days,
    decay_rate,
    meals_per_day
):
    results = []

    for _ in range(n_sim):
        life_age = np.random.normal(life_mean, life_std)
        remaining_years = max(life_age - mom_age, 0)

        years_abroad = min(abroad_years, remaining_years)
        years_domestic = max(remaining_years - abroad_years, 0)

        total_days = 0
        total_meals = 0

        # abroad phase
        for y in range(int(years_abroad)):
            age = mom_age + y
            visits = np.random.poisson(visits_per_year)
            decay = np.exp(-decay_rate * (age - mom_age))
            days = visits * days_per_visit * decay

            total_days += days
            total_meals += days * meals_per_day

        # domestic phase
        for y in range(int(years_domestic)):
            age = mom_age + years_abroad + y
            decay = np.exp(-decay_rate * (age - mom_age))
            days = domestic_days * decay

            total_days += days
            total_meals += days * meals_per_day

        results.append([remaining_years, total_days, total_meals])

    arr = np.array(results)

    return {
        "years": arr[:, 0],
        "days": arr[:, 1],
        "meals": arr[:, 2],
        "total_days_mean": arr[:, 1].mean()
    }