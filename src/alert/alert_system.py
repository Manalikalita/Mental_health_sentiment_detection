# src/alert/alert_system.py

class AlertSystem:

    def __init__(self, high=0.75, medium=0.5):
        self.high = high
        self.medium = medium

    def generate_alert(self, label, confidence):

        if label in ["depression", "anxiety"] and confidence > self.high:
            return "HIGH"

        elif confidence > self.medium:
            return "MEDIUM"

        else:
            return "LOW"