import re
from schema import TripRequest

BLOCKED_PATTERNS = [
    r"ignore (all )?(previous|prior) instructions",
    r"reveal (your )?(system prompt|hidden instructions)",
    r"bypass (all )?(guardrails|safety)",
]

def validate_request(data: dict) -> TripRequest:
    request = TripRequest.model_validate(data)

    text = f"{request.destination} {request.interests}"

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            raise ValueError(
                "Please provide travel preferences only."
            )

    return request