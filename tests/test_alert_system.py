from src.alert.alert_system import AlertSystem


def test_suicidal_label_always_high():
    alert_system = AlertSystem()

    assert alert_system.generate_alert("suicidal", 0.37) == "HIGH"
    assert alert_system.generate_alert("Suicidal", 0.01) == "HIGH"
    assert alert_system.generate_alert("suicide", 0.2) == "HIGH"


def test_high_risk_label_confidence_thresholds():
    alert_system = AlertSystem()

    assert alert_system.generate_alert("depression", 0.8) == "HIGH"
    assert alert_system.generate_alert("anxiety", 0.6) == "MEDIUM"
    assert alert_system.generate_alert("depression", 0.3) == "MEDIUM"
    assert alert_system.generate_alert("anxiety", 0.1) == "MEDIUM"


def test_stress_label_uses_risk_thresholds():
    alert_system = AlertSystem()

    assert alert_system.generate_alert("stress", 0.8) == "HIGH"
    assert alert_system.generate_alert("stress", 0.6) == "MEDIUM"
    assert alert_system.generate_alert("stress", 0.2) == "LOW"
