const API_URL = "http://127.0.0.1:8000";

let missionHistory = [];

// Load previous history when website opens
document.addEventListener("DOMContentLoaded", () => {
    loadHistory();
});


// ======================================================
// RUN MISSION
// ======================================================

async function runMission() {

    const button = document.getElementById("runButton");
    const loading = document.getElementById("loading");

    button.disabled = true;

    if (loading) {
        loading.classList.remove("hidden");
        loading.textContent = "Running multi-agent mission...";
    }

    setText("decisionBox", "⏳ MISSION RUNNING...");

    try {

        console.log("Connecting to FastAPI...");

        const response = await fetch(
            `${API_URL}/mission/run`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    drone_id: "DRONE-01"
                })
            }
        );

        console.log("Response status:", response.status);

        if (!response.ok) {
            throw new Error(
                `Server returned ${response.status}`
            );
        }

        const data = await response.json();

        console.log("MISSION RESPONSE:");
        console.log(data);

        if (!data.success) {
            throw new Error(
                data.error || "Mission failed."
            );
        }

        displayMissionResult(data);

    }

    catch (error) {

        console.error("MISSION ERROR:", error);

        setText(
            "decisionBox",
            "❌ MISSION ERROR: " + error.message
        );

        alert(
            "Mission failed.\n\n" +
            error.message
        );

    }

    finally {

        button.disabled = false;

        if (loading) {
            loading.classList.add("hidden");
        }
    }
}


// ======================================================
// DISPLAY MISSION RESULT
// ======================================================

function displayMissionResult(data) {

    console.log("Displaying mission result:", data);

    const result = data.result || data;

    // ------------------------------------------
    // TELEMETRY
    // ------------------------------------------

    const telemetry =
        result.telemetry ||
        data.telemetry ||
        {};

    updateTelemetry(telemetry);


    // ------------------------------------------
    // DIAGNOSIS
    // ------------------------------------------

    const diagnosis =
        result.diagnosis ||
        data.diagnosis ||
        {};

    setText(
        "diagnosis",
        formatResult(diagnosis)
    );


    // ------------------------------------------
    // RECOVERY
    // ------------------------------------------

    const recovery =
        result.recovery_plan ||
        result.recovery ||
        data.recovery_plan ||
        {};

    setText(
        "recovery",
        formatResult(recovery)
    );


    // ------------------------------------------
    // SAFETY
    // ------------------------------------------

    const safety =
        result.safety_result ||
        result.safety ||
        data.safety_result ||
        {};

    setText(
        "safety",
        formatResult(safety)
    );


    // ------------------------------------------
    // RAG KNOWLEDGE
    // ------------------------------------------

    const knowledge =
        result.knowledge ||
        result.rag_result ||
        data.knowledge ||
        [];

    setText(
        "knowledge",
        formatResult(knowledge)
    );


    // ------------------------------------------
    // FINAL STATUS
    // ------------------------------------------

    const status =
        result.mission_status ||
        result.status ||
        data.mission_status ||
        "MISSION COMPLETED";

    updateMissionStatus(status);


    // ------------------------------------------
    // ADD TO HISTORY
    // ------------------------------------------

    addMissionToHistory(
        telemetry,
        diagnosis,
        status
    );
}


// ======================================================
// UPDATE TELEMETRY
// ======================================================

function updateTelemetry(telemetry) {

    setText(
        "droneId",
        telemetry.drone_id || "DRONE-01"
    );

    setText(
        "mission",
        telemetry.mission || "Solar Panel Inspection"
    );

    setText(
        "battery",
        telemetry.battery !== undefined
            ? telemetry.battery + " %"
            : "-- %"
    );

    setText(
        "temperature",
        telemetry.temperature !== undefined
            ? telemetry.temperature + " °C"
            : "-- °C"
    );

    setText(
        "gps",
        telemetry.gps || "--"
    );

    setText(
        "motor",
        telemetry.motor || "--"
    );

    setText(
        "altitude",
        telemetry.altitude !== undefined
            ? telemetry.altitude + " m"
            : "-- m"
    );

    setText(
        "scenario",
        telemetry.scenario || "--"
    );


    // Visual status

    updateTelemetryClass(
        "battery",
        telemetry.battery
    );

    updateTelemetryClass(
        "temperature",
        telemetry.temperature
    );

    updateGPSStatus(
        telemetry.gps
    );

    updateMotorStatus(
        telemetry.motor
    );
}


// ======================================================
// MISSION STATUS
// ======================================================

function updateMissionStatus(status) {

    const box = document.getElementById(
        "decisionBox"
    );

    if (!box) return;

    box.textContent =
        "MISSION STATUS: " + status;

    box.classList.remove(
        "status-safe",
        "status-warning",
        "status-danger"
    );


    if (
        status === "AUTONOMOUS_ACTION_ALLOWED"
    ) {

        box.classList.add(
            "status-safe"
        );

    }

    else if (
        status === "HUMAN_APPROVAL_REQUIRED"
    ) {

        box.classList.add(
            "status-danger"
        );

    }

    else {

        box.classList.add(
            "status-warning"
        );
    }
}


// ======================================================
// TELEMETRY COLORS
// ======================================================

function updateTelemetryClass(
    id,
    value
) {

    const element =
        document.getElementById(id);

    if (!element) return;

    element.classList.remove(
        "value-safe",
        "value-warning",
        "value-danger"
    );


    if (id === "battery") {

        if (value < 30) {

            element.classList.add(
                "value-danger"
            );

        }

        else if (value < 50) {

            element.classList.add(
                "value-warning"
            );

        }

        else {

            element.classList.add(
                "value-safe"
            );
        }
    }


    if (id === "temperature") {

        if (value >= 80) {

            element.classList.add(
                "value-danger"
            );

        }

        else if (value >= 65) {

            element.classList.add(
                "value-warning"
            );

        }

        else {

            element.classList.add(
                "value-safe"
            );
        }
    }
}


function updateGPSStatus(gps) {

    const element =
        document.getElementById("gps");

    if (!element) return;

    element.classList.remove(
        "value-safe",
        "value-danger"
    );

    if (gps === "ONLINE") {

        element.classList.add(
            "value-safe"
        );

    }

    else if (gps === "OFFLINE") {

        element.classList.add(
            "value-danger"
        );
    }
}


function updateMotorStatus(motor) {

    const element =
        document.getElementById("motor");

    if (!element) return;

    element.classList.remove(
        "value-safe",
        "value-warning",
        "value-danger"
    );


    if (motor === "NORMAL") {

        element.classList.add(
            "value-safe"
        );

    }

    else if (motor === "WARNING") {

        element.classList.add(
            "value-warning"
        );

    }

    else if (motor === "FAILURE") {

        element.classList.add(
            "value-danger"
        );
    }
}


// ======================================================
// MISSION HISTORY
// ======================================================

function addMissionToHistory(
    telemetry,
    diagnosis,
    status
) {

    const time =
        new Date().toLocaleTimeString();

    let severity =
        "LOW";

    if (
        diagnosis &&
        typeof diagnosis === "object"
    ) {

        severity =
            diagnosis.severity ||
            "LOW";
    }


    const mission = {

        time: time,

        scenario:
            telemetry.scenario ||
            "UNKNOWN",

        severity: severity,

        status: status
    };


    missionHistory.unshift(
        mission
    );


    // Keep only last 10 missions

    if (missionHistory.length > 10) {

        missionHistory =
            missionHistory.slice(
                0,
                10
            );
    }


    localStorage.setItem(
        "droneMissionHistory",
        JSON.stringify(
            missionHistory
        )
    );


    renderMissionHistory();
}


// ======================================================
// LOAD HISTORY
// ======================================================

function loadHistory() {

    const saved =
        localStorage.getItem(
            "droneMissionHistory"
        );

    if (saved) {

        try {

            missionHistory =
                JSON.parse(saved);

        }

        catch {

            missionHistory = [];
        }
    }

    renderMissionHistory();
}


// ======================================================
// DISPLAY HISTORY
// ======================================================

function renderMissionHistory() {

    const container =
        document.getElementById(
            "missionHistory"
        );

    if (!container) return;


    if (missionHistory.length === 0) {

        container.innerHTML =
            "<p>No missions executed yet.</p>";

        return;
    }


    container.innerHTML =
        missionHistory
            .map((mission) => {

                let statusClass =
                    "history-warning";

                if (
                    mission.status ===
                    "AUTONOMOUS_ACTION_ALLOWED"
                ) {

                    statusClass =
                        "history-safe";
                }

                if (
                    mission.status ===
                    "HUMAN_APPROVAL_REQUIRED"
                ) {

                    statusClass =
                        "history-danger";
                }


                return `

                    <div class="history-item">

                        <div class="history-time">
                            ${mission.time}
                        </div>

                        <div class="history-scenario">
                            ${mission.scenario}
                        </div>

                        <div class="history-severity">
                            ${mission.severity}
                        </div>

                        <div class="${statusClass}">
                            ${mission.status}
                        </div>

                    </div>

                `;

            })
            .join("");
}


// ======================================================
// HELPER
// ======================================================

function setText(
    id,
    value
) {

    const element =
        document.getElementById(id);

    if (element) {

        element.textContent =
            value;
    }
}


// ======================================================
// FORMAT OBJECTS
// ======================================================

function formatResult(value) {

    if (
        value === undefined ||
        value === null ||
        value === ""
    ) {

        return "No data available.";
    }


    if (
        typeof value === "string"
    ) {

        return value;
    }


    try {

        return JSON.stringify(
            value,
            null,
            2
        );

    }

    catch {

        return String(value);
    }
}