import random
from datetime import datetime


class DroneSimulator:

    def __init__(self, drone_id="DRONE-01"):
        self.drone_id = drone_id
        self.mission = "Solar Panel Inspection"

    def generate_telemetry(self, scenario=None):
        """
        Generate simulated drone telemetry.

        If scenario is provided, that specific failure
        scenario is generated.

        If scenario is not provided, a random scenario
        is generated.
        """

        scenarios = [
            "NORMAL",
            "LOW_BATTERY",
            "MOTOR_FAILURE",
            "OVERHEATING",
            "GPS_FAILURE"
        ]

        # Random scenario when no scenario is specified
        if scenario is None:
            scenario = random.choice(scenarios)

        # Validate scenario
        scenario = scenario.upper()

        if scenario not in scenarios:
            raise ValueError(
                f"Invalid scenario: {scenario}. "
                f"Choose from: {scenarios}"
            )

        # ---------------------------------------------
        # NORMAL MISSION
        # ---------------------------------------------

        if scenario == "NORMAL":

            battery = random.randint(70, 100)
            temperature = random.randint(35, 55)
            gps = "ONLINE"
            motor = "NORMAL"

        # ---------------------------------------------
        # LOW BATTERY
        # ---------------------------------------------

        elif scenario == "LOW_BATTERY":

            battery = random.randint(10, 25)
            temperature = random.randint(40, 60)
            gps = "ONLINE"
            motor = "NORMAL"

        # ---------------------------------------------
        # MOTOR FAILURE
        # ---------------------------------------------

        elif scenario == "MOTOR_FAILURE":

            battery = random.randint(30, 80)
            temperature = random.randint(50, 75)
            gps = "ONLINE"
            motor = "FAILURE"

        # ---------------------------------------------
        # OVERHEATING
        # ---------------------------------------------

        elif scenario == "OVERHEATING":

            battery = random.randint(30, 80)
            temperature = random.randint(80, 100)
            gps = "ONLINE"
            motor = "WARNING"

        # ---------------------------------------------
        # GPS FAILURE
        # ---------------------------------------------

        elif scenario == "GPS_FAILURE":

            battery = random.randint(30, 80)
            temperature = random.randint(40, 60)
            gps = "OFFLINE"
            motor = "NORMAL"

        # ---------------------------------------------
        # TELEMETRY
        # ---------------------------------------------

        return {
            "drone_id": self.drone_id,
            "mission": self.mission,
            "scenario": scenario,
            "battery": battery,
            "temperature": temperature,
            "gps": gps,
            "motor": motor,
            "altitude": random.randint(50, 120),
            "timestamp": datetime.now().isoformat()
        }


# =====================================================
# DIRECT SIMULATOR TEST
# =====================================================

if __name__ == "__main__":

    drone = DroneSimulator()

    print()
    print("=" * 55)
    print("       AUTONOMOUS DRONE SIMULATOR")
    print("=" * 55)

    telemetry = drone.generate_telemetry()

    print()

    for key, value in telemetry.items():
        print(f"{key:15}: {value}")