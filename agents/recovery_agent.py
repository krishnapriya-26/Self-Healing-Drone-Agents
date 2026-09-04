from memory.mission_memory import MissionMemory


class RecoveryAgent:

    def __init__(self):
        self.memory = MissionMemory()

    def generate_recovery_plan(
        self,
        telemetry,
        diagnosis,
        knowledge
    ):

        scenario = telemetry.get(
            "scenario",
            "UNKNOWN"
        )

        # -------------------------------------------------
        # Retrieve previous similar missions
        # -------------------------------------------------

        previous_missions = (
            self.memory.find_similar_missions(
                scenario
            )
        )

        previous_action = (
            self.memory.get_previous_action(
                scenario
            )
        )

        # -------------------------------------------------
        # Default recovery decision
        # -------------------------------------------------

        action = "CONTINUE_MISSION"

        priority = "LOW"

        reason = (
            "Drone telemetry is within "
            "normal operating limits."
        )

        # -------------------------------------------------
        # LOW BATTERY
        # -------------------------------------------------

        if scenario == "LOW_BATTERY":

            action = "RETURN_TO_BASE"

            priority = "HIGH"

            reason = (
                "Battery level is too low "
                "for safe mission continuation."
            )

        # -------------------------------------------------
        # MOTOR FAILURE
        # -------------------------------------------------

        elif scenario == "MOTOR_FAILURE":

            action = "ABORT_MISSION"

            priority = "CRITICAL"

            reason = (
                "Motor failure detected. "
                "Continuing the inspection may "
                "compromise flight stability."
            )

        # -------------------------------------------------
        # OVERHEATING
        # -------------------------------------------------

        elif scenario == "OVERHEATING":

            action = "LAND_AND_COOL"

            priority = "HIGH"

            reason = (
                "High temperature detected. "
                "Drone should stop the mission "
                "and reduce thermal load."
            )

        # -------------------------------------------------
        # GPS FAILURE
        # -------------------------------------------------

        elif scenario == "GPS_FAILURE":

            action = "HOLD_AND_REQUEST_HUMAN"

            priority = "CRITICAL"

            reason = (
                "GPS signal is unavailable. "
                "Autonomous navigation cannot "
                "be considered reliable."
            )

        # -------------------------------------------------
        # NORMAL
        # -------------------------------------------------

        elif scenario == "NORMAL":

            action = "CONTINUE_MISSION"

            priority = "LOW"

            reason = (
                "Telemetry indicates normal "
                "flight conditions."
            )

        # -------------------------------------------------
        # USE PREVIOUS MEMORY
        # -------------------------------------------------

        memory_used = False

        if previous_action:

            memory_used = True

            memory_note = (
                "A previous mission with the same "
                f"failure used the action: "
                f"{previous_action}"
            )

        else:

            memory_note = (
                "No previous mission with this "
                "failure scenario was found."
            )

        # -------------------------------------------------
        # Return recovery plan
        # -------------------------------------------------

        return {

            "scenario": scenario,

            "priority": priority,

            "recommended_action": action,

            "reason": reason,

            "previous_action": previous_action,

            "similar_missions":
                len(previous_missions),

            "memory_used": memory_used,

            "memory_note": memory_note,

            "knowledge_used":
                len(knowledge)
                if isinstance(knowledge, list)
                else 0
        }


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    agent = RecoveryAgent()

    telemetry = {

        "drone_id": "DRONE-01",

        "mission":
            "Solar Panel Inspection",

        "scenario":
            "GPS_FAILURE",

        "battery": 65,

        "temperature": 52,

        "gps": "OFFLINE",

        "motor": "NORMAL",

        "altitude": 90
    }

    diagnosis = {

        "severity": "CRITICAL",

        "problem":
            "GPS signal lost"
    }

    knowledge = [

        {
            "source":
                "gps_failure.txt",

            "content":
                "Request human intervention "
                "when autonomous navigation "
                "cannot be trusted."
        }
    ]

    result = agent.generate_recovery_plan(

        telemetry,

        diagnosis,

        knowledge
    )

    print()
    print("=" * 60)
    print("             RECOVERY AGENT")
    print("=" * 60)

    for key, value in result.items():

        print(
            f"{key:22}: {value}"
        )

    print()
    print("=" * 60)