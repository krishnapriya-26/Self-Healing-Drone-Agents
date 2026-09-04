from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from data.drone_simulator import DroneSimulator
from agents.diagnosis_agent import DiagnosisAgent
from agents.rag_agent import RAGAgent
from agents.recovery_agent import RecoveryAgent
from agents.safety_agent import SafetyAgent


# ============================================================
# DRONE WORKFLOW STATE
# ============================================================

class DroneState(TypedDict, total=False):
    drone_id: str
    telemetry: dict
    diagnosis: Any
    knowledge: list
    previous_missions: list
    recovery_plan: Any
    safety_result: Any
    mission_status: str


# ============================================================
# INITIALIZE COMPONENTS
# ============================================================

drone = DroneSimulator()

diagnosis_agent = DiagnosisAgent()

rag_agent = RAGAgent()

recovery_agent = RecoveryAgent()

safety_agent = SafetyAgent()


# ============================================================
# 1. TELEMETRY AGENT
# ============================================================

def telemetry_node(state: DroneState):

    drone_id = state.get("drone_id", "DRONE-01")

    drone.drone_id = drone_id

    telemetry = drone.generate_telemetry()

    print()
    print("=" * 60)
    print("[TELEMETRY AGENT]")
    print("=" * 60)

    print("Drone ID:", telemetry.get("drone_id"))
    print("Scenario:", telemetry.get("scenario"))
    print("Battery:", telemetry.get("battery"), "%")
    print("Temperature:", telemetry.get("temperature"), "°C")
    print("GPS:", telemetry.get("gps"))
    print("Motor:", telemetry.get("motor"))
    print("Altitude:", telemetry.get("altitude"), "m")

    return {
        "drone_id": drone_id,
        "telemetry": telemetry
    }


# ============================================================
# 2. DIAGNOSIS AGENT
# ============================================================

def diagnosis_node(state: DroneState):

    telemetry = state.get("telemetry", {})

    print()
    print("=" * 60)
    print("[DIAGNOSIS AGENT]")
    print("=" * 60)

    # Try the method used by the existing diagnosis agent
    try:
        diagnosis = diagnosis_agent.diagnose(telemetry)
    except AttributeError:

        try:
            diagnosis = diagnosis_agent.analyze(telemetry)
        except AttributeError:

            diagnosis = {
                "scenario": telemetry.get("scenario"),
                "problem": telemetry.get("scenario"),
                "status": "DIAGNOSIS_COMPLETED"
            }

    print("Diagnosis:", diagnosis)

    return {
        "diagnosis": diagnosis
    }


# ============================================================
# 3. RAG KNOWLEDGE AGENT
# ============================================================

def rag_node(state: DroneState):

    telemetry = state.get("telemetry", {})

    diagnosis = state.get("diagnosis", {})

    scenario = telemetry.get(
        "scenario",
        "UNKNOWN"
    )

    print()
    print("=" * 60)
    print("[RAG KNOWLEDGE AGENT]")
    print("=" * 60)

    # RAG agent receives the problem/scenario
    try:
        knowledge = rag_agent.retrieve(scenario)
    except Exception:

        try:
            knowledge = rag_agent.retrieve(
                str(diagnosis)
            )
        except Exception:
            knowledge = []

    # Make sure knowledge is always a list
    if knowledge is None:
        knowledge = []

    if isinstance(knowledge, dict):
        knowledge = [knowledge]

    print("Scenario:", scenario)
    print("Knowledge retrieved:", len(knowledge))

    return {
        "knowledge": knowledge
    }


# ============================================================
# 4. MISSION MEMORY
# ============================================================

def memory_node(state: DroneState):

    telemetry = state.get("telemetry", {})

    scenario = telemetry.get(
        "scenario",
        "UNKNOWN"
    )

    print()
    print("=" * 60)
    print("[MISSION MEMORY]")
    print("=" * 60)

    previous_missions = []

    try:

        from memory.mission_memory import MissionMemory

        memory = MissionMemory()

        # Try common memory methods
        try:
            previous_missions = memory.search(scenario)

        except AttributeError:

            try:
                previous_missions = memory.retrieve(scenario)

            except AttributeError:
                previous_missions = []

    except Exception:
        previous_missions = []

    if previous_missions is None:
        previous_missions = []

    if isinstance(previous_missions, dict):
        previous_missions = [previous_missions]

    print(
        "Previous missions:",
        len(previous_missions)
    )

    return {
        "previous_missions": previous_missions
    }


# ============================================================
# 5. RECOVERY AGENT
# ============================================================

def recovery_node(state: DroneState):

    telemetry = state.get(
        "telemetry",
        {}
    )

    diagnosis = state.get(
        "diagnosis",
        {}
    )

    knowledge = state.get(
        "knowledge",
        []
    )

    previous_missions = state.get(
        "previous_missions",
        []
    )

    print()
    print("=" * 60)
    print("[RECOVERY AGENT]")
    print("=" * 60)

    try:

        recovery_plan = recovery_agent.plan_recovery(
            telemetry=telemetry,
            diagnosis=diagnosis,
            knowledge=knowledge,
            previous_missions=previous_missions
        )

    except AttributeError:

        try:

            recovery_plan = recovery_agent.recover(
                telemetry,
                diagnosis,
                knowledge
            )

        except AttributeError:

            recovery_plan = {
                "action": "HOLD_AND_REQUEST_HUMAN",
                "reason": "Recovery agent requires human approval"
            }

    print(
        "Recovery plan:",
        recovery_plan
    )

    return {
        "recovery_plan": recovery_plan
    }


# ============================================================
# 6. SAFETY AGENT
# ============================================================

def safety_node(state: DroneState):

    telemetry = state.get(
        "telemetry",
        {}
    )

    recovery_plan = state.get(
        "recovery_plan",
        {}
    )

    print()
    print("=" * 60)
    print("[SAFETY AGENT]")
    print("=" * 60)

    try:

        safety_result = safety_agent.evaluate(
            telemetry=telemetry,
            recovery_plan=recovery_plan
        )

    except AttributeError:

        try:

            safety_result = safety_agent.check(
                telemetry,
                recovery_plan
            )

        except AttributeError:

            # Conservative default
            safety_result = {
                "human_intervention": True,
                "action": "HOLD_AND_REQUEST_HUMAN",
                "message": "Human approval required"
            }

    if safety_result is None:
        safety_result = {}

    print(
        "Safety result:",
        safety_result
    )

    # ========================================================
    # DETERMINE MISSION STATUS
    # ========================================================

    if isinstance(safety_result, dict):

        human_required = safety_result.get(
            "human_intervention",
            False
        )

        action = safety_result.get(
            "action",
            ""
        )

        if (
            human_required
            or action == "HOLD_AND_REQUEST_HUMAN"
        ):

            mission_status = (
                "HUMAN_APPROVAL_REQUIRED"
            )

        else:

            mission_status = (
                "AUTONOMOUS_ACTION_ALLOWED"
            )

    else:

        mission_status = (
            "HUMAN_APPROVAL_REQUIRED"
        )

    print(
        "Mission status:",
        mission_status
    )

    return {
        "safety_result": safety_result,
        "mission_status": mission_status
    }


# ============================================================
# BUILD LANGGRAPH
# ============================================================

workflow = StateGraph(DroneState)


# ============================================================
# ADD NODES
# ============================================================

workflow.add_node(
    "telemetry_agent",
    telemetry_node
)

workflow.add_node(
    "diagnosis_agent",
    diagnosis_node
)

workflow.add_node(
    "rag_agent",
    rag_node
)

workflow.add_node(
    "memory_agent",
    memory_node
)

workflow.add_node(
    "recovery_agent",
    recovery_node
)

workflow.add_node(
    "safety_agent",
    safety_node
)


# ============================================================
# CONNECT NODES
# ============================================================

workflow.add_edge(
    START,
    "telemetry_agent"
)

workflow.add_edge(
    "telemetry_agent",
    "diagnosis_agent"
)

workflow.add_edge(
    "diagnosis_agent",
    "rag_agent"
)

workflow.add_edge(
    "rag_agent",
    "memory_agent"
)

workflow.add_edge(
    "memory_agent",
    "recovery_agent"
)

workflow.add_edge(
    "recovery_agent",
    "safety_agent"
)

workflow.add_edge(
    "safety_agent",
    END
)


# ============================================================
# COMPILE WORKFLOW
# ============================================================

drone_workflow = workflow.compile()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("SELF-HEALING MULTI-AGENT DRONE PLATFORM")
    print("=" * 70)

    result = drone_workflow.invoke(
        {
            "drone_id": "DRONE-01"
        }
    )

    print()
    print("=" * 70)
    print("FINAL MISSION RESULT")
    print("=" * 70)

    print()
    print("Drone ID:")
    print(
        result.get(
            "drone_id"
        )
    )

    print()
    print("Telemetry:")
    print(
        result.get(
            "telemetry"
        )
    )

    print()
    print("Diagnosis:")
    print(
        result.get(
            "diagnosis"
        )
    )

    print()
    print("RAG Knowledge:")
    print(
        result.get(
            "knowledge"
        )
    )

    print()
    print("Previous Missions:")
    print(
        result.get(
            "previous_missions"
        )
    )

    print()
    print("Recovery Plan:")
    print(
        result.get(
            "recovery_plan"
        )
    )

    print()
    print("Safety Result:")
    print(
        result.get(
            "safety_result"
        )
    )

    print()
    print("Mission Status:")
    print(
        result.get(
            "mission_status"
        )
    )

    print()
    print("=" * 70)
    print("WORKFLOW COMPLETED")
    print("=" * 70)