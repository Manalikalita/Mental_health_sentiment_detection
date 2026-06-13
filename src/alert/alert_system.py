class AlertSystem:

    def __init__(self, high=0.75, medium=0.5):
        self.high = high
        self.medium = medium

    def generate_alert(self, label, confidence):

        suicidal_labels = {"suicidal", "suicide"}
        medium_risk_labels = {"depression", "anxiety", "stress"}

        label = label.lower()

        if label in suicidal_labels:
            return "HIGH"

        if label in medium_risk_labels:
            if confidence >= self.high:
                return "HIGH"
            if confidence >= self.medium:
                return "MEDIUM"
            return "LOW"

        return "LOW"