from data.drone_simulator import DroneSimulator

from agents.telemetry_agent import TelemetryAgent
from agents.diagnosis_agent import DiagnosisAgent
from agents.rag_agent import RAGAgent
from agents.recovery_agent import RecoveryAgent
from agents.safety_agent import SafetyAgent


def main():

    print("\n==============================================")
    print("   SELF-HEALING MULTI-AGENT DRONE PLATFORM")
    print("==============================================")

    # ------------------------------------------------
    # 1. DRONE
    # ------------------------------------------------

    drone = DroneSimulator()

    telemetry = drone.generate_telemetry()

    print("\n[1] DRONE TELEMETRY")

    print(f"Drone ID     : {telemetry['drone_id']}")
    print(f"Mission      : {telemetry['mission']}")
    print(f"Battery      : {telemetry['battery']}%")
    print(f"Temperature  : {telemetry['temperature']}°C")
    print(f"GPS          : {telemetry['gps']}")
    print(f"Motor        : {telemetry['motor']}")
    print(f"Scenario     : {telemetry['scenario']}")

    # ------------------------------------------------
    # 2. TELEMETRY AGENT
    # ------------------------------------------------

    telemetry_agent = TelemetryAgent()

    findings = telemetry_agent.analyze(telemetry)

    print("\n[2] TELEMETRY AGENT")

    for finding in findings:
        print(f"• {finding}")

    # ------------------------------------------------
    # 3. DIAGNOSIS AGENT
    # ------------------------------------------------

    diagnosis_agent = DiagnosisAgent()

    diagnosis = diagnosis_agent.diagnose(
        telemetry,
        findings
    )

    print("\n[3] DIAGNOSIS AGENT")

    print(diagnosis["diagnosis"])

    # ------------------------------------------------
    # 4. RAG AGENT
    # ------------------------------------------------

    rag_agent = RAGAgent()

    query = diagnosis["diagnosis"]

    retrieved_knowledge = rag_agent.retrieve(
        query
    )

    print("\n[4] RAG AGENT")

    print("Relevant recovery knowledge retrieved:")

    for result in retrieved_knowledge:
        print("\n---")
        print(result[:300])

    # ------------------------------------------------
    # 5. RECOVERY AGENT
    # ------------------------------------------------

    recovery_agent = RecoveryAgent()

    recovery_plan = recovery_agent.create_recovery_plan(
        diagnosis,
        retrieved_knowledge
    )

    print("\n[5] RECOVERY AGENT")

    print(
        f"Recommended Action: "
        f"{recovery_plan['recommended_action']}"
    )

    # ------------------------------------------------
    # 6. SAFETY AGENT
    # ------------------------------------------------

    safety_agent = SafetyAgent()

    safety_result = safety_agent.validate(
        recovery_plan
    )

    print("\n[6] SAFETY AGENT")

    print(
        f"Status: {safety_result['status']}"
    )

    print(
        f"Action: {safety_result['action']}"
    )

    print("\n==============================================")
    print("              MISSION DECISION")
    print("==============================================")

    if safety_result["approved"]:

        print(
            f"✓ Autonomous action allowed: "
            f"{safety_result['action']}"
        )

    else:

        print(
            "⚠ HUMAN APPROVAL REQUIRED"
        )

        print(
            f"Requested action: "
            f"{safety_result['action']}"
        )

    print("\n==============================================")


if __name__ == "__main__":
    main()