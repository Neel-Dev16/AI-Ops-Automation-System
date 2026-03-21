import re


# Group 1 keeps the Bearer prefix so only the token value is replaced.
BEARER_TOKEN_PATTERN = re.compile(r"(Bearer\s+)[^\s]+", re.IGNORECASE)

# Group 1 captures the field name and equals sign so the key stays readable.
API_KEY_PATTERN = re.compile(r"(api_key=)[^\s&]+", re.IGNORECASE)

# Group 1 captures the field name and equals sign so the key stays readable.
PASSWORD_PATTERN = re.compile(r"(password=)[^\s&]+", re.IGNORECASE)

# Group 1 captures the field name and equals sign so the key stays readable.
TOKEN_PATTERN = re.compile(r"(token=)[^\s&]+", re.IGNORECASE)

# Group 1 preserves the header label and separator while redacting the value.
AUTHORIZATION_HEADER_PATTERN = re.compile(
    r"(Authorization:\s*)[^\r\n]+", re.IGNORECASE
)

EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def redact_sensitive_data(text: str) -> str:
    redacted_text = text or ""

    redacted_text = EMAIL_PATTERN.sub("[EMAIL_REDACTED]", redacted_text)
    redacted_text = BEARER_TOKEN_PATTERN.sub(r"\1[TOKEN_REDACTED]", redacted_text)
    redacted_text = API_KEY_PATTERN.sub(r"\1[REDACTED]", redacted_text)
    redacted_text = PASSWORD_PATTERN.sub(r"\1[REDACTED]", redacted_text)
    redacted_text = TOKEN_PATTERN.sub(r"\1[REDACTED]", redacted_text)
    redacted_text = AUTHORIZATION_HEADER_PATTERN.sub(
        r"\1[REDACTED]", redacted_text
    )

    return redacted_text
