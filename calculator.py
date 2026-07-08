from dataclasses import dataclass

# ==========================================================
# Assumptions
# ==========================================================

EXPECTED_RETURN = 0.12          # 12%
INFLATION = 0.06                # 6%
SAFE_WITHDRAWAL_RATE = 0.04     # 4%

REAL_RETURN = (
    (1 + EXPECTED_RETURN) /
    (1 + INFLATION)
) - 1


# ==========================================================
# Output
# ==========================================================

@dataclass
class FireResult:
    fire_number: float
    projected_corpus: float
    gap: float
    years_left: int
    on_track: bool
    progress_percent: float
    required_monthly_investment: float


# ==========================================================
# Calculator
# ==========================================================

def calculate_fire(
    age: int,
    retirement_age: int,
    current_corpus: float,
    monthly_investment: float,
    annual_expenses: float,
):

    years_left = retirement_age - age

    fire_number = annual_expenses / SAFE_WITHDRAWAL_RATE

    corpus = current_corpus

    # Grow investments year by year
    for _ in range(years_left):
        corpus *= (1 + REAL_RETURN)
        corpus += monthly_investment * 12

    gap = max(0, fire_number - corpus)

    progress = min(
        corpus / fire_number * 100,
        100,
    )

    # Future value of current investments only
    future_value_current = (
        current_corpus *
        ((1 + REAL_RETURN) ** years_left)
    )

    remaining = max(
        0,
        fire_number - future_value_current,
    )

    if years_left > 0 and REAL_RETURN > 0:

        annuity_factor = (
            ((1 + REAL_RETURN) ** years_left - 1)
            / REAL_RETURN
        )

        required_monthly = (
            remaining /
            annuity_factor /
            12
        )

    else:
        required_monthly = 0

    return FireResult(
        fire_number=round(fire_number, 2),
        projected_corpus=round(corpus, 2),
        gap=round(gap, 2),
        years_left=years_left,
        on_track=corpus >= fire_number,
        progress_percent=round(progress, 1),
        required_monthly_investment=round(required_monthly, 2),
    )