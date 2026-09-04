import os
from dotenv import load_dotenv

load_dotenv()


class DiagnosisAgent:

    def diagnose(self, telemetry, findings=None):

        # If workflow does not provide findings,
        # create an empty list automatically.
        if findings is None:
            findings = []

        scenario = telemetry.get("scenario", "NORMAL")

        # -----------------------------------------
        # LOW BATTERY
        # -----------------------------------------

        if scenario == "LOW_BATTERY":

            diagnosis = (
                "Critical low-battery condition detected. "
                "The drone may not have enough energy to "
                "safely continue the current mission."
            )

            severity = "CRITICAL"

        # -----------------------------------------
        # MOTOR FAILURE
        # -----------------------------------------

        elif scenario == "MOTOR_FAILURE":

            diagnosis = (
                "Critical motor failure detected. "
                "Continuing the inspection mission may "
                "compromise flight stability."
            )

            severity = "CRITICAL"

        # -----------------------------------------
        # OVERHEATING
        # -----------------------------------------

        elif scenario == "OVERHEATING":

            diagnosis = (
                "High temperature detected. "
                "Continued operation may cause hardware "
                "damage or system instability."
            )

            severity = "HIGH"

        # -----------------------------------------
        # GPS FAILURE
        # -----------------------------------------

        elif scenario == "GPS_FAILURE":

            diagnosis = (
                "GPS signal failure detected. "
                "Autonomous navigation reliability is reduced."
            )

            severity = "HIGH"

        # -----------------------------------------
        # NORMAL
        # -----------------------------------------

        else:

            diagnosis = (
                "No critical failure detected. "
                "The drone can continue the mission."
            )

            severity = "LOW"

        # -----------------------------------------
        # RETURN DIAGNOSIS
        # -----------------------------------------

        return {
            "scenario": scenario,
            "severity": severity,
            "findings": findings,
            "diagnosis": diagnosis
        }


# ---------------------------------------------
# TEST THE AGENT DIRECTLY
# ---------------------------------------------

if __name__ == "__main__":

    agent = DiagnosisAgent()

    test_telemetry = {
        "drone_id": "DRONE-01",
        "mission": "Solar Panel Inspection",
        "scenario": "LOW_BATTERY",
        "battery": 18,
        "temperature": 50,
        "gps": "ONLINE",
        "motor": "NORMAL",
        "altitude": 80
    }

    result = agent.diagnose(test_telemetry)

    print("\n==============================")
    print("DIAGNOSIS AGENT TEST")
    print("==============================")

    for key, value in result.items():
        print(f"{key}: {value}")