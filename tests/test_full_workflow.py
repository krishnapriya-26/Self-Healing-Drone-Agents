from data.drone_simulator import DroneSimulator
from workflow.drone_workflow import app


def run_scenario(scenario):

    print()
    print("=" * 70)
    print(f"             SCENARIO: {scenario}")
    print("=" * 70)

    # Create simulator
    drone = DroneSimulator()

    # Generate specific telemetry
    telemetry = drone.generate_telemetry(
        scenario
    )

    print()
    print("[TELEMETRY]")
    print("-" * 70)

    for key, value in telemetry.items():
        print(f"{key:15}: {value}")

    # Run complete LangGraph workflow
    result = app.invoke({
        "telemetry": telemetry
    })

    # -----------------------------------------------
    # DIAGNOSIS
    # -----------------------------------------------

    diagnosis = result.get(
        "diagnosis",
        {}
    )

    print()
    print("[DIAGNOSIS AGENT]")
    print("-" * 70)

    if isinstance(diagnosis, dict):

        for key, value in diagnosis.items():

            print(
                f"{key:15}: {value}"
            )

    else:

        print(diagnosis)

    # -----------------------------------------------
    # RAG
    # -----------------------------------------------

    knowledge = result.get(
        "knowledge",
        []
    )

    print()
    print("[RAG AGENT]")
    print("-" * 70)

    print(
        f"Retrieved documents: {len(knowledge)}"
    )

    for item in knowledge[:2]:

        if isinstance(item, dict):

            print(
                f"Source: {item.get('source', 'unknown')}"
            )

            print(
                item.get('content', '')[:200]
            )

        else:

            print(
                str(item)[:200]
            )

    # -----------------------------------------------
    # MEMORY
    # -----------------------------------------------

    memory = result.get(
        "previous_missions",
        []
    )

    print()
    print("[MISSION MEMORY]")
    print("-" * 70)

    print(
        f"Previous similar missions: {len(memory)}"
    )

    # -----------------------------------------------
    # RECOVERY
    # -----------------------------------------------

    recovery = result.get(
        "recovery_plan",
        {}
    )

    print()
    print("[RECOVERY AGENT]")
    print("-" * 70)

    if isinstance(recovery, dict):

        for key, value in recovery.items():

            print(
                f"{key:20}: {value}"
            )

    else:

        print(recovery)

    # -----------------------------------------------
    # SAFETY
    # -----------------------------------------------

    safety = result.get(
        "safety_result",
        {}
    )

    print()
    print("[SAFETY AGENT]")
    print("-" * 70)

    if isinstance(safety, dict):

        for key, value in safety.items():

            print(
                f"{key:20}: {value}"
            )

    else:

        print(safety)

    print()
    print("=" * 70)


def main():

    scenarios = [

        "NORMAL",

        "LOW_BATTERY",

        "MOTOR_FAILURE",

        "OVERHEATING",

        "GPS_FAILURE"

    ]

    print()
    print("#" * 70)
    print(
        "   SELF-HEALING MULTI-AGENT DRONE TEST"
    )
    print("#" * 70)

    for scenario in scenarios:

        try:

            run_scenario(
                scenario
            )

        except Exception as error:

            print()
            print(
                f"ERROR in {scenario}:"
            )

            print(error)

    print()
    print("#" * 70)
    print(
        "              TESTING COMPLETE"
    )
    print("#" * 70)


if __name__ == "__main__":

    main()