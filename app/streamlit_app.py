import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from time_with_mom.simulator import simulate

st.title("Time with Mom Simulator")

# Sidebar
mom_age = st.sidebar.slider("Mom Age", 40, 90, 60)
life_mean = st.sidebar.slider("Expected Lifespan", 70, 100, 85)
life_std = st.sidebar.slider("Lifespan Uncertainty", 1, 10, 5)
abroad_years = st.sidebar.slider("Years Abroad", 0, 30, 10)

visits_per_year = st.sidebar.slider("Visits per Year", 0.0, 5.0, 1.0)
days_per_visit = st.sidebar.slider("Days per Visit", 1, 90, 30)
domestic_days = st.sidebar.slider("Domestic Days per Year", 0, 365, 120)

decay_rate = st.sidebar.slider("Decay Rate", 0.0, 0.1, 0.03)
meals_per_day = st.sidebar.slider("Meals per Day", 1, 5, 2)
n_sim = st.sidebar.slider("Simulation Runs", 1000, 20000, 5000)

if st.button("Run Simulation"):

    data = simulate(
        n_sim=n_sim,
        mom_age=mom_age,
        life_mean=life_mean,
        life_std=life_std,
        abroad_years=abroad_years,
        visits_per_year=visits_per_year,
        days_per_visit=days_per_visit,
        domestic_days=domestic_days,
        decay_rate=decay_rate,
        meals_per_day=meals_per_day
    )

    # =====================
    # ✅ Results（恢复）
    # =====================
    avg_years = data["years"].mean()
    avg_days = data["days"].mean()
    avg_meals = data["meals"].mean()

    p10, p90 = np.percentile(data["days"], [10, 90])

    st.subheader("Results")

    st.write(f"Remaining Years (avg): {avg_years:.1f}")
    st.write(f"Total Days Together (avg): {avg_days:.0f}")
    st.write(f"Total Days (10%-90%): {p10:.0f} - {p90:.0f}")
    st.write(f"Total Meals (avg): {avg_meals:.0f}")

    # =====================
    # ✅ Equivalence Insight（恢复）
    # =====================
    required_days = domestic_days / max(visits_per_year, 0.01)

    st.subheader("Equivalence Insight")

    st.write(f"Each visit should be ~ {required_days:.0f} days")

    ratio = (visits_per_year * days_per_visit) / domestic_days
    st.write(f"Current ratio: {ratio:.2%}")

    # =====================
    # ✅ Plot（你原来的）
    # =====================
    visits_range = np.linspace(0.5, 4, 10)
    results_curve = []

    for v in visits_range:
        temp = simulate(
            n_sim=2000,
            mom_age=mom_age,
            life_mean=life_mean,
            life_std=life_std,
            abroad_years=abroad_years,
            visits_per_year=v,
            days_per_visit=days_per_visit,
            domestic_days=domestic_days,
            decay_rate=decay_rate,
            meals_per_day=meals_per_day
        )
        results_curve.append(temp["total_days_mean"])

    plt.figure()
    plt.plot(visits_range, results_curve)
    plt.xlabel("Visits per Year")
    plt.ylabel("Total Days Together")

    st.pyplot(plt)

    # =====================
    # ✅ Strategy（恢复）
    # =====================
    if ratio < 0.5:
        st.warning("Significant gap vs domestic life")
    elif ratio < 0.8:
        st.info("Moderate gap")
    else:
        st.success("Close to domestic level")