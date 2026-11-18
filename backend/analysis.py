def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """Calculate BMI as a descriptive measurement, not a diagnosis."""
    height_m = height_cm / 100
    if height_m <= 0:
        raise ValueError("Height must be positive")
    return round(weight_kg / (height_m ** 2), 2)

def assess_measurement(age_years: float, bmi: float) -> tuple[str, str]:
    """
    Avoids assigning malnutrition categories from BMI alone.
    Adult BMI thresholds are not used for children/adolescents.
    """
    if age_years < 20:
        return (
            "reference_required",
            "For people under 20, BMI must be interpreted using age- and sex-specific "
            "growth references. This demo does not calculate growth z-scores or diagnose."
        )
    return (
        "review_required",
        "BMI is a screening measurement only. A qualified health professional must "
        "interpret it alongside clinical history and other nutritional indicators."
    )
