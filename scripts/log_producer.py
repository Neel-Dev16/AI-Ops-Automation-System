from __future__ import annotations

import itertools
import time
from dataclasses import dataclass

import requests


API_URL = "http://127.0.0.1:8000/api/logs/ingest"
SLEEP_SECONDS = 2


@dataclass
class LogEvent:
    service_name: str
    environment: str
    level: str
    message: str
    source: str


LOG_EVENTS = [
    LogEvent(
        service_name="payment-service",
        environment="production",
        level="ERROR",
        message="Database timeout after 30s while processing checkout.",
        source="payment-api",
    ),
    LogEvent(
        service_name="payment-service",
        environment="production",
        level="CRITICAL",
        message="Connection pool exhausted during payment authorization.",
        source="payment-worker",
    ),
    LogEvent(
        service_name="auth-service",
        environment="production",
        level="WARN",
        message="JWT token expired for user session refresh request.",
        source="auth-api",
    ),
    LogEvent(
        service_name="auth-service",
        environment="production",
        level="ERROR",
        message="Unauthorized access attempt detected on admin endpoint.",
        source="auth-gateway",
    ),
    LogEvent(
        service_name="inventory-service",
        environment="production",
        level="CRITICAL",
        message="OOM killed worker process while rebuilding stock cache.",
        source="inventory-worker",
    ),
    LogEvent(
        service_name="payment-service",
        environment="production",
        level="ERROR",
        message="Payment failed after downstream gateway returned service unavailable.",
        source="payment-api",
    ),
    LogEvent(
        service_name="frontend-service",
        environment="development",
        level="INFO",
        message="Health check passed for storefront UI.",
        source="frontend",
    ),
    LogEvent(
        service_name="frontend-service",
        environment="development",
        level="INFO",
        message="Request completed successfully for product listing page.",
        source="frontend",
    ),
    LogEvent(
        service_name="database-service",
        environment="production",
        level="WARN",
        message="Connection pool exhausted warning triggered on replica node.",
        source="db-monitor",
    ),
    LogEvent(
        service_name="database-service",
        environment="production",
        level="ERROR",
        message="Database timeout observed during analytics query execution.",
        source="db-proxy",
    ),
]


def send_log(event: LogEvent) -> None:
    payload = {
        "service_name": event.service_name,
        "environment": event.environment,
        "level": event.level,
        "message": event.message,
        "source": event.source,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        print(
            f"[{event.level}] {event.service_name}: {event.message} "
            f"-> {response.status_code}"
        )
        print(response.text)
    except requests.RequestException as exc:
        print(f"Request failed for {event.service_name}: {exc}")


def main() -> None:
    print(f"Sending logs to {API_URL}")
    print("Press Ctrl+C to stop.")

    try:
        for event in itertools.cycle(LOG_EVENTS):
            send_log(event)
            time.sleep(SLEEP_SECONDS)
    except KeyboardInterrupt:
        print("\nLog producer stopped.")


if __name__ == "__main__":
    main()
