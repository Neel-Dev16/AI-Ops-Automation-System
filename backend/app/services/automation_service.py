from app.schemas import IncidentAnalysisResult


def apply_automation_rules(analysis: IncidentAnalysisResult) -> dict:
    if analysis.severity == "critical":
        return {
            "priority_score": 100,
            "automation_action": "immediate_escalation",
            "escalation_message": (
                "Critical incident detected. Notify the on-call engineer immediately and begin emergency response."
            ),
        }

    if analysis.severity == "high":
        return {
            "priority_score": 80,
            "automation_action": "escalate_to_engineering",
            "escalation_message": (
                "High-severity incident detected. Escalate to the engineering team for urgent investigation."
            ),
        }

    if analysis.severity == "medium":
        return {
            "priority_score": 50,
            "automation_action": "create_investigation_task",
            "escalation_message": (
                "Investigation recommended but immediate escalation is not required."
            ),
        }

    return {
        "priority_score": 20,
        "automation_action": "monitor_only",
        "escalation_message": "No escalation required. Continue monitoring.",
    }
