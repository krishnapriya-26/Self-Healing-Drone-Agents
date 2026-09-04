class TelemetryAgent:

    def analyze(self, telemetry):

        findings = []

        battery = telemetry["battery"]
        temperature = telemetry["temperature"]
        gps = telemetry["gps"]
        motor = telemetry["motor"]

        if battery < 20:
            findings.append("CRITICAL: Low battery")

        elif battery < 30:
            findings.append("WARNING: Battery level is low")

        if temperature > 80:
            findings.append("CRITICAL: High temperature")

        elif temperature > 70:
            findings.append("WARNING: Temperature is elevated")

        if gps == "OFFLINE":
            findings.append("CRITICAL: GPS connection lost")

        if motor == "FAILURE":
            findings.append("CRITICAL: Motor failure detected")

        elif motor == "WARNING":
            findings.append("WARNING: Motor status abnormal")

        if not findings:
            findings.append("Telemetry status normal")

        return findings