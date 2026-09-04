import json
from pathlib import Path
from datetime import datetime


class MissionMemory:

    def __init__(self):

        self.memory_dir = Path("memory")

        self.memory_dir.mkdir(
            exist_ok=True
        )

        self.memory_file = (
            self.memory_dir / "mission_history.json"
        )

        if not self.memory_file.exists():

            self.memory_file.write_text(
                "[]",
                encoding="utf-8"
            )


    # =====================================================
    # LOAD PREVIOUS MISSIONS
    # =====================================================

    def load_missions(self):

        try:

            data = json.loads(
                self.memory_file.read_text(
                    encoding="utf-8"
                )
            )

            if isinstance(data, list):

                return data

            return []

        except Exception:

            return []


    # =====================================================
    # SAVE MISSION
    # =====================================================

    def save_mission(
        self,
        drone_id,
        scenario,
        diagnosis,
        action,
        result
    ):

        missions = self.load_missions()

        mission = {

            "drone_id": drone_id,

            "scenario": scenario,

            "diagnosis": diagnosis,

            "action": action,

            "result": result,

            "timestamp":
                datetime.now().isoformat()
        }

        missions.append(
            mission
        )

        self.memory_file.write_text(

            json.dumps(
                missions,
                indent=4
            ),

            encoding="utf-8"
        )

        return mission


    # =====================================================
    # FIND SIMILAR MISSIONS
    # =====================================================

    def find_similar_missions(
        self,
        scenario
    ):

        missions = self.load_missions()

        matches = []

        for mission in missions:

            if (
                mission.get("scenario")
                == scenario
            ):

                matches.append(
                    mission
                )

        # Return latest 5 similar missions

        return matches[-5:]


    # =====================================================
    # GET PREVIOUS ACTION
    # =====================================================

    def get_previous_action(
        self,
        scenario
    ):

        matches = self.find_similar_missions(
            scenario
        )

        if not matches:

            return None

        return matches[-1].get(
            "action"
        )


    # =====================================================
    # MEMORY SUMMARY
    # =====================================================

    def get_summary(self):

        missions = self.load_missions()

        summary = {

            "total_missions":
                len(missions),

            "scenarios": {}
        }

        for mission in missions:

            scenario = mission.get(
                "scenario",
                "UNKNOWN"
            )

            if scenario not in summary[
                "scenarios"
            ]:

                summary["scenarios"][
                    scenario
                ] = 0

            summary["scenarios"][
                scenario
            ] += 1

        return summary


# =========================================================
# DIRECT MEMORY TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("          MISSION MEMORY TEST")
    print("=" * 60)

    memory = MissionMemory()

    # Save a test mission

    memory.save_mission(

        drone_id="DRONE-TEST",

        scenario="GPS_FAILURE",

        diagnosis="GPS signal lost",

        action="HOLD_AND_REQUEST_HUMAN",

        result="HUMAN_APPROVAL_REQUIRED"
    )

    print()
    print("Mission saved successfully.")

    # Search memory

    previous = memory.find_similar_missions(
        "GPS_FAILURE"
    )

    print()
    print(
        "Previous GPS failure missions:",
        len(previous)
    )

    for mission in previous:

        print()
        print(
            "Scenario:",
            mission["scenario"]
        )

        print(
            "Diagnosis:",
            mission["diagnosis"]
        )

        print(
            "Previous Action:",
            mission["action"]
        )

        print(
            "Result:",
            mission["result"]
        )

    print()
    print("Memory Summary:")
    print(
        memory.get_summary()
    )

    print()
    print("=" * 60)