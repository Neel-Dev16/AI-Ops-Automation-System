import json

from openai import OpenAI

from app.config import LLM_MODE, OPENAI_API_KEY, OPENAI_MODEL
from app.schemas import IncidentAnalysisResult


def analyze_logs_with_mock(raw_logs: str) -> IncidentAnalysisResult:
    normalized_logs = raw_logs.lower()

    if any(keyword in normalized_logs for keyword in ["timeout", "connection pool", "database"]):
        return IncidentAnalysisResult(
            service_name="payment-service",
            severity="high",
            incident_type="database_timeout",
            summary="Database timeout or connection pool issue detected in the logs.",
            root_cause="Database connection pool exhaustion or timeout",
            recommended_actions="Check database pool settings, inspect slow queries, and review database availability.",
            requires_escalation=True,
        )

    if any(keyword in normalized_logs for keyword in ["jwt", "unauthorized", "authentication"]):
        return IncidentAnalysisResult(
            service_name="auth-service",
            severity="medium",
            incident_type="authentication_failure",
            summary="Authentication-related failures were detected in the logs.",
            root_cause="Authentication token validation failure",
            recommended_actions="Review JWT validation, inspect token expiry settings, and verify authentication middleware.",
            requires_escalation=False,
        )

    if any(keyword in normalized_logs for keyword in ["memory", "oom", "out of memory"]):
        return IncidentAnalysisResult(
            service_name="inventory-service",
            severity="critical",
            incident_type="memory_exhaustion",
            summary="Memory exhaustion symptoms were detected in the logs.",
            root_cause="Service is running out of memory",
            recommended_actions="Check memory usage, inspect recent deployments, and increase or optimize service resources.",
            requires_escalation=True,
        )

    return IncidentAnalysisResult(
        service_name="unknown-service",
        severity="low",
        incident_type="general_warning",
        summary="The logs contain a general warning without a clear incident pattern.",
        root_cause="No clear root cause detected",
        recommended_actions="Review the logs manually and gather more context before taking action.",
        requires_escalation=False,
    )


def analyze_logs_with_openai(raw_logs: str) -> IncidentAnalysisResult:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Set it before using LLM_MODE=openai.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    "You are an AIOps incident analyst. Analyze raw application logs and "
                    "return only valid JSON that matches the requested schema."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Analyze these logs and return JSON only.\n\n"
                    f"Raw logs:\n{raw_logs}"
                ),
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "incident_analysis_result",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "service_name": {"type": "string"},
                        "severity": {
                            "type": "string",
                            "enum": ["critical", "high", "medium", "low"],
                        },
                        "incident_type": {"type": "string"},
                        "summary": {"type": "string"},
                        "root_cause": {"type": "string"},
                        "recommended_actions": {"type": "string"},
                        "requires_escalation": {"type": "boolean"},
                    },
                    "required": [
                        "service_name",
                        "severity",
                        "incident_type",
                        "summary",
                        "root_cause",
                        "recommended_actions",
                        "requires_escalation",
                    ],
                    "additionalProperties": False,
                },
            }
        },
    )

    output_text = getattr(response, "output_text", "")
    if not output_text:
        raise ValueError("OpenAI returned an empty response.")

    try:
        parsed_json = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise ValueError("OpenAI returned invalid JSON.") from exc

    try:
        return IncidentAnalysisResult.model_validate(parsed_json)
    except Exception as exc:
        raise ValueError("OpenAI returned JSON that does not match IncidentAnalysisResult.") from exc


def analyze_logs_with_llm(raw_logs: str) -> IncidentAnalysisResult:
    if LLM_MODE == "openai":
        return analyze_logs_with_openai(raw_logs)

    return analyze_logs_with_mock(raw_logs)
