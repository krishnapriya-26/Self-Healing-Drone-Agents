class SafetyAgent:

    def __init__(self):
        self.critical_scenarios = {
            "MOTOR_FAILURE",
            "GPS_FAILURE"
        }

        self.high_risk_scenarios = {
            "LOW_BATTERY",
            "OVERHEATING"
        }

    def evaluate(
        self,
        telemetry,
        recovery_plan
    ):

        scenario = telemetry.get(
            "scenario",
            "UNKNOWN"
        )

        proposed_action = recovery_plan.get(
            "recommended_action",
            "UNKNOWN"
        )

        # -------------------------------------------------
        # CRITICAL FAILURE
        # -------------------------------------------------

        if scenario in self.critical_scenarios:

            return {
                "status": "HUMAN_APPROVAL_REQUIRED",
                "risk_level": "CRITICAL",
                "approved_action": "STOP_AUTONOMOUS_OPERATION",
                "reason": (
                    f"{scenario} is a critical safety condition. "
                    "Autonomous operation requires human intervention."
                ),
                "human_intervention": True
            }

        # -------------------------------------------------
        # HIGH-RISK CONDITION
        # -------------------------------------------------

        if scenario in self.high_risk_scenarios:

            return {
                "status": "SAFE_AUTONOMOUS_ACTION",
                "risk_level": "HIGH",
                "approved_action": proposed_action,
                "reason": (
                    f"{scenario} requires an immediate "
                    "protective recovery action."
                ),
                "human_intervention": False
            }

        # -------------------------------------------------
        # NORMAL OPERATION
        # -------------------------------------------------

        if scenario == "NORMAL":

            return {
                "status": "AUTONOMOUS_ACTION_ALLOWED",
                "risk_level": "LOW",
                "approved_action": "CONTINUE_MISSION",
                "reason": (
                    "Telemetry is within normal operating "
                    "conditions."
                ),
                "human_intervention": False
            }

        # -------------------------------------------------
        # UNKNOWN CONDITION
        # -------------------------------------------------

        return {
            "status": "HUMAN_APPROVAL_REQUIRED",
            "risk_level": "UNKNOWN",
            "approved_action": "PAUSE_MISSION",
            "reason": (
                "Unknown scenario detected. "
                "The system will fail safely and request "
                "human review."
            ),
            "human_intervention": True
        }


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    agent = SafetyAgent()

    test_scenarios = [
        "NORMAL",
        "LOW_BATTERY",
        "MOTOR_FAILURE",
        "OVERHEATING",
        "GPS_FAILURE"
    ]

    for scenario in test_scenarios:

        telemetry = {
            "drone_id": "DRONE-01",
            "scenario": scenario
        }

        recovery_plan = {
            "recommended_action": {
                "NORMAL": "CONTINUE_MISSION",
                "LOW_BATTERY": "RETURN_TO_BASE",
                "MOTOR_FAILURE": "ABORT_MISSION",
                "OVERHEATING": "LAND_AND_COOL",
                "GPS_FAILURE": "HOLD_AND_REQUEST_HUMAN"
            }.get(
                scenario,
                "UNKNOWN"
            )
        }

        result = agent.evaluate(
            telemetry,
            recovery_plan
        )

        print()
        print("=" * 65)
        print(f"SCENARIO: {scenario}")
        print("=" * 65)

        for key, value in result.items():

            print(
                f"{key:25}: {value}"
            )