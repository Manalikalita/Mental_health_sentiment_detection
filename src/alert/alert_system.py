class AlertSystem:

    def __init__(self, high=0.75, medium=0.5):
        self.high = high
        self.medium = medium

    def generate_alert(self, label, confidence):

        high_risk_labels = ["suicidal", "depression", "anxiety"]

        label = label.lower()

        if label in high_risk_labels and confidence > self.high:
            return "HIGH"

        elif confidence > self.medium:
            return "MEDIUM"

        else:
            return "LOW"