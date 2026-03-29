import argparse
import numpy as np
from .simulator import simulate


def cmd_simulate(args):
    data = simulate(
        n_sim=args.n_sim,
        mom_age=args.mom_age,
        life_mean=args.life_mean,
        life_std=args.life_std,
        abroad_years=args.abroad_years,
        visits_per_year=args.visits,
        days_per_visit=args.days,
        domestic_days=args.domestic_days,
        decay_rate=args.decay,
        meals_per_day=args.meals,
    )

    avg_days = data["days"].mean()
    p10, p90 = np.percentile(data["days"], [10, 90])

    ratio = (args.visits * args.days) / max(args.domestic_days, 1)

    print("\n=== Simulation Result ===")
    print(f"Avg total days: {avg_days:.0f}")
    print(f"10%-90% range: {p10:.0f} - {p90:.0f}")
    print(f"Ratio vs domestic: {ratio:.2%}")

    if ratio < 0.5:
        print("→ Significant gap vs domestic life")
    elif ratio < 0.8:
        print("→ Moderate gap")
    else:
        print("→ Close to domestic level")


def cmd_optimize(args):
    visits_range = np.linspace(0.5, args.max_visits, args.steps)
    best = None
    best_days = -1

    for v in visits_range:
        data = simulate(
            n_sim=args.n_sim,
            mom_age=args.mom_age,
            life_mean=args.life_mean,
            life_std=args.life_std,
            abroad_years=args.abroad_years,
            visits_per_year=v,
            days_per_visit=args.days,
            domestic_days=args.domestic_days,
            decay_rate=args.decay,
            meals_per_day=args.meals,
        )
        avg_days = data["days"].mean()

        if avg_days > best_days:
            best_days = avg_days
            best = v

    print("\n=== Optimization Result ===")
    print(f"Best visits/year: {best:.2f}")
    print(f"Expected total days: {best_days:.0f}")


def cmd_plot(args):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed. pip install matplotlib")
        return

    visits_range = np.linspace(0.5, args.max_visits, args.steps)
    results = []

    for v in visits_range:
        data = simulate(
            n_sim=args.n_sim,
            mom_age=args.mom_age,
            life_mean=args.life_mean,
            life_std=args.life_std,
            abroad_years=args.abroad_years,
            visits_per_year=v,
            days_per_visit=args.days,
            domestic_days=args.domestic_days,
            decay_rate=args.decay,
            meals_per_day=args.meals,
        )
        results.append(data["total_days_mean"])

    plt.plot(visits_range, results)
    plt.xlabel("Visits per Year")
    plt.ylabel("Total Days Together")
    plt.title("Sensitivity Curve")
    plt.show()


def build_parser():
    parser = argparse.ArgumentParser(
        prog="time-with-mom",
        description="Time with Mom Simulation Toolkit",
    )

    subparsers = parser.add_subparsers(dest="command")

    def add_common(p):
        p.add_argument("--mom-age", type=int, default=60)
        p.add_argument("--life-mean", type=int, default=85)
        p.add_argument("--life-std", type=int, default=5)
        p.add_argument("--abroad-years", type=int, default=10)
        p.add_argument("--days", type=int, default=30)
        p.add_argument("--domestic-days", type=int, default=120)
        p.add_argument("--decay", type=float, default=0.03)
        p.add_argument("--meals", type=int, default=2)
        p.add_argument("--n-sim", type=int, default=3000)

    # simulate
    p_sim = subparsers.add_parser("simulate")
    add_common(p_sim)
    p_sim.add_argument("--visits", type=float, default=1.0)
    p_sim.set_defaults(func=cmd_simulate)

    # optimize
    p_opt = subparsers.add_parser("optimize")
    add_common(p_opt)
    p_opt.add_argument("--max-visits", type=float, default=4.0)
    p_opt.add_argument("--steps", type=int, default=10)
    p_opt.set_defaults(func=cmd_optimize)

    # plot
    p_plot = subparsers.add_parser("plot")
    add_common(p_plot)
    p_plot.add_argument("--max-visits", type=float, default=4.0)
    p_plot.add_argument("--steps", type=int, default=10)
    p_plot.set_defaults(func=cmd_plot)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()