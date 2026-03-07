from __future__ import annotations

from dataclasses import dataclass

import requests


API_URL = "http://127.0.0.1:8000/api/logs/analyze"


@dataclass
class TestCase:
    name: str
    raw_logs: str
    expected_severity: str
    expected_incident_type: str
    expected_requires_escalation: bool


TEST_CASES = [
    TestCase(
        name="Database timeout",
        raw_logs="ERROR payment-service database timeout after 30s. Connection pool exhausted.",
        expected_severity="high",
        expected_incident_type="database_timeout",
        expected_requires_escalation=True,
    ),
    TestCase(
        name="Authentication failure",
        raw_logs="WARN auth-service unauthorized request. JWT validation failed for access token.",
        expected_severity="medium",
        expected_incident_type="authentication_failure",
        expected_requires_escalation=False,
    ),
    TestCase(
        name="Memory exhaustion",
        raw_logs="CRITICAL inventory-service out of memory. OOM killed worker process.",
        expected_severity="critical",
        expected_incident_type="memory_exhaustion",
        expected_requires_escalation=True,
    ),
    TestCase(
        name="General warning",
        raw_logs="WARN gateway-service transient retry observed but request completed successfully.",
        expected_severity="low",
        expected_incident_type="general_warning",
        expected_requires_escalation=False,
    ),
]


def bool_label(value: bool) -> str:
    return "yes" if value else "no"


def fetch_analysis(raw_logs: str) -> dict:
    response = requests.post(API_URL, json={"raw_logs": raw_logs}, timeout=10)
    response.raise_for_status()
    return response.json()


def print_table(results: list[dict]) -> None:
    header = (
        f"{'Case':<24}"
        f"{'Severity':<20}"
        f"{'Type':<34}"
        f"{'Escalation':<22}"
    )
    print(header)
    print("-" * len(header))

    for result in results:
        severity_column = (
            f"{result['actual_severity']} "
            f"({'OK' if result['severity_match'] else 'MISS'})"
        )
        type_column = (
            f"{result['actual_incident_type']} "
            f"({'OK' if result['incident_type_match'] else 'MISS'})"
        )
        escalation_column = (
            f"{bool_label(result['actual_requires_escalation'])} "
            f"({'OK' if result['escalation_match'] else 'MISS'})"
        )

        print(
            f"{result['name']:<24}"
            f"{severity_column:<20}"
            f"{type_column:<34}"
            f"{escalation_column:<22}"
        )


def print_accuracy(results: list[dict]) -> None:
    total = len(results)
    severity_hits = sum(result["severity_match"] for result in results)
    type_hits = sum(result["incident_type_match"] for result in results)
    escalation_hits = sum(result["escalation_match"] for result in results)

    print()
    print("Accuracy Summary")
    print(f"- Severity: {severity_hits}/{total} ({severity_hits / total:.0%})")
    print(f"- Incident Type: {type_hits}/{total} ({type_hits / total:.0%})")
    print(f"- Escalation Decision: {escalation_hits}/{total} ({escalation_hits / total:.0%})")


def main() -> None:
    results: list[dict] = []

    try:
        for case in TEST_CASES:
            analysis = fetch_analysis(case.raw_logs)
            results.append(
                {
                    "name": case.name,
                    "actual_severity": analysis["severity"],
                    "actual_incident_type": analysis["incident_type"],
                    "actual_requires_escalation": analysis["requires_escalation"],
                    "severity_match": analysis["severity"] == case.expected_severity,
                    "incident_type_match": analysis["incident_type"] == case.expected_incident_type,
                    "escalation_match": (
                        analysis["requires_escalation"] == case.expected_requires_escalation
                    ),
                }
            )
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        print("Make sure the backend server is running on http://127.0.0.1:8000.")
        return

    print_table(results)
    print_accuracy(results)


if __name__ == "__main__":
    main()
