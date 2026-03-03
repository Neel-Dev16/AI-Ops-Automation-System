from app.schemas import IncidentAnalysisResult


def analyze_logs_with_llm(raw_logs: str) -> IncidentAnalysisResult:
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
