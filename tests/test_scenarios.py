from data.drone_simulator import DroneSimulator


def print_telemetry(telemetry):

    print()
    print("-" * 60)

    print(
        f"Scenario: {telemetry['scenario']}"
    )

    print(
        f"Battery: {telemetry['battery']}%"
    )

    print(
        f"Temperature: {telemetry['temperature']}°C"
    )

    print(
        f"GPS: {telemetry['gps']}"
    )

    print(
        f"Motor: {telemetry['motor']}"
    )

    print(
        f"Altitude: {telemetry['altitude']} m"
    )


def main():

    drone = DroneSimulator()

    scenarios = [
        "NORMAL",
        "LOW_BATTERY",
        "MOTOR_FAILURE",
        "OVERHEATING",
        "GPS_FAILURE"
    ]

    print()
    print("=" * 60)
    print("       DRONE FAILURE SCENARIO TESTING")
    print("=" * 60)

    for scenario in scenarios:

        telemetry = drone.generate_telemetry(
            scenario
        )

        print_telemetry(
            telemetry
        )

    print()
    print("=" * 60)
    print("       ALL SCENARIOS TESTED")
    print("=" * 60)


if __name__ == "__main__":
    main()