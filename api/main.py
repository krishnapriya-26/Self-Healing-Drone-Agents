from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from workflow.drone_workflow import drone_workflow


# ==================================================
# CREATE FASTAPI APP
# ==================================================

api = FastAPI(
    title="Self-Healing Drone Multi-Agent API",
    description="API for autonomous drone mission monitoring and recovery",
    version="1.0.0"
)


# ==================================================
# CORS
# ==================================================

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# REQUEST MODEL
# ==================================================

class MissionRequest(BaseModel):
    drone_id: str = "DRONE-01"


# ==================================================
# HELPER FUNCTION
# Find telemetry anywhere inside workflow result
# ==================================================

def find_telemetry(data):

    if isinstance(data, dict):

        # Direct telemetry dictionary
        if (
            "battery" in data
            and "temperature" in data
            and "gps" in data
        ):
            return {
                "drone_id": data.get("drone_id", "DRONE-01"),
                "mission": data.get(
                    "mission",
                    "Solar Panel Inspection"
                ),
                "scenario": data.get("scenario", "UNKNOWN"),
                "battery": data.get("battery"),
                "temperature": data.get("temperature"),
                "gps": data.get("gps"),
                "motor": data.get("motor"),
                "altitude": data.get("altitude"),
                "timestamp": data.get("timestamp")
            }

        # Search nested dictionaries
        for value in data.values():

            result = find_telemetry(value)

            if result is not None:
                return result


    elif isinstance(data, list):

        for item in data:

            result = find_telemetry(item)

            if result is not None:
                return result


    return None


# ==================================================
# HOME
# ==================================================

@api.get("/")
def home():

    return {
        "message": "Self-Healing Drone API is running",
        "status": "ONLINE"
    }


# ==================================================
# HEALTH CHECK
# ==================================================

@api.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "Self-Healing Drone API"
    }


# ==================================================
# RUN MISSION
# ==================================================

@api.post("/mission/run")
def run_mission(request: MissionRequest):

    print("\n")
    print("==========================================")
    print("        SELF-HEALING DRONE MISSION")
    print("==========================================")

    print(f"Drone ID: {request.drone_id}")

    try:

        # ------------------------------------------
        # Workflow input
        # ------------------------------------------

        workflow_input = {
            "drone_id": request.drone_id
        }


        # ------------------------------------------
        # Execute LangGraph workflow
        # ------------------------------------------

        result = drone_workflow.invoke(workflow_input)


        # ------------------------------------------
        # Extract telemetry
        # ------------------------------------------

        telemetry = find_telemetry(result)


        print("\n[TELEMETRY]")

        if telemetry:

            print(
                f"Battery: {telemetry.get('battery')} %"
            )

            print(
                f"Temperature: "
                f"{telemetry.get('temperature')} °C"
            )

            print(
                f"GPS: {telemetry.get('gps')}"
            )

            print(
                f"Motor: {telemetry.get('motor')}"
            )

            print(
                f"Altitude: {telemetry.get('altitude')} m"
            )

            print(
                f"Scenario: {telemetry.get('scenario')}"
            )

        else:

            print("Telemetry could not be extracted.")


        # ------------------------------------------
        # Mission completed
        # ------------------------------------------

        print("\n[MISSION CONTROLLER]")
        print("Mission decision completed.")


        # ------------------------------------------
        # Send clean response to frontend
        # ------------------------------------------

        return {
            "success": True,

            "drone_id": request.drone_id,

            "telemetry": telemetry,

            "result": result
        }


    except Exception as error:

        print("\n[ERROR]")
        print(str(error))


        return {
            "success": False,

            "drone_id": request.drone_id,

            "telemetry": None,

            "error": str(error)
        }