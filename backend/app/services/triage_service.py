SUSPICIOUS_KEYWORDS = [
    "out of memory",
    "oom",
    "service unavailable",
    "database timeout",
    "connection pool",
    "payment failed",
    "authentication failed",
    "unauthorized",
]

UNKNOWN_LEVEL_KEYWORDS = [
    "failed",
    "exception",
    "timeout",
]


def triage_log(level: str, message: str, environment: str = "development") -> dict:
    normalized_level = (level or "").strip().upper()
    normalized_message = (message or "").lower()
    normalized_environment = (environment or "").strip().lower()

    if normalized_level in {"CRITICAL", "FATAL"}:
        result = {
            "triage_decision": "analyze",
            "risk_score": 95,
            "reason": "Critical or fatal log level requires immediate analysis.",
        }
    elif normalized_level == "ERROR":
        result = {
            "triage_decision": "analyze",
            "risk_score": 80,
            "reason": "Error-level log should be analyzed for incident detection.",
        }
    elif normalized_level in {"WARN", "WARNING"}:
        result = {
            "triage_decision": "store_only",
            "risk_score": 45,
            "reason": "Warning-level log should be stored for later review.",
        }
    elif normalized_level in {"INFO", "DEBUG"}:
        result = {
            "triage_decision": "ignore",
            "risk_score": 10,
            "reason": "Informational or debug log does not require triage.",
        }
    else:
        result = {
            "triage_decision": "store_only",
            "risk_score": 25,
            "reason": "Unknown log level was stored for reference.",
        }

    if any(keyword in normalized_message for keyword in SUSPICIOUS_KEYWORDS):
        result["triage_decision"] = "analyze"
        result["risk_score"] = max(result["risk_score"], 85)
        result["reason"] = "Message contains a high-risk operational keyword."
    elif normalized_level not in {"CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG"}:
        if any(keyword in normalized_message for keyword in UNKNOWN_LEVEL_KEYWORDS):
            result["triage_decision"] = "analyze"
            result["risk_score"] = 70
            result["reason"] = "Unknown log level contains suspicious failure keywords."

    if normalized_environment == "production" and result["triage_decision"] != "ignore":
        result["risk_score"] = min(result["risk_score"] + 10, 100)
        result["reason"] += " Production environment increased the risk score."

    return result
