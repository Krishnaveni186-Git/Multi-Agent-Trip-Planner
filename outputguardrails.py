def validate_draft(draft: str, budget_inr: int) -> list[str]:
    warnings = []

    if not draft or len(draft.strip()) < 80:
        warnings.append("The itinerary is too short.")

    if "estimate" not in draft.lower():
        warnings.append(
            "The plan should identify costs as estimates."
        )

    if "₹" not in draft and "inr" not in draft.lower():
        warnings.append("Add an INR cost breakdown.")

    return warnings