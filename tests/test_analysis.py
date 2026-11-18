from backend.analysis import calculate_bmi, assess_measurement

def test_bmi_calculation():
    assert calculate_bmi(170, 70) == 24.22

def test_child_requires_growth_reference():
    status, message = assess_measurement(12, 18.5)
    assert status == "reference_required"
    assert "age- and sex-specific" in message

def test_adult_requires_professional_review():
    status, _ = assess_measurement(25, 22)
    assert status == "review_required"
