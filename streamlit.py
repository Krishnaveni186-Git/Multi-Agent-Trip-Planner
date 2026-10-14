import streamlit as st
from dotenv import load_dotenv
from schema import TripRequest
from inputguardrail import validate_request
from outputguardrails import validate_draft
from agents import create_trip_plan

load_dotenv()
st.set_page_config(page_title="Multi-Agent Trip Planner", page_icon="🧳", layout="wide")
st.title("🧳 Multi-Agent Trip Planner")
st.caption("LangGraph + Gemini + Streamlit | Human approval and guardrails")

with st.sidebar:
    st.header("How it works")
    st.markdown(
        "1. Validate trip details\n"
        "2. Research Agent\n"
        "3. Itinerary Agent\n"
        "4. Budget Agent\n"
        "5. Review Agent\n"
        "6. You approve or request changes"
    )
    st.info("AI-generated travel suggestions are not live booking, availability, or price confirmations.")

if "draft" not in st.session_state:
    st.session_state.draft = None
if "request" not in st.session_state:
    st.session_state.request = None
if "approved" not in st.session_state:
    st.session_state.approved = False
if "warnings" not in st.session_state:
    st.session_state.warnings = []

with st.form("trip_form"):
    st.subheader("Tell us about your trip")
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Destination", placeholder=" ")
        start_date = st.date_input("Start date")
        travelers = st.number_input("Number of travelers", min_value=1, max_value=20, value=2)
        budget = st.number_input("Total budget (INR)", min_value=1000, max_value=10_000_000, value=15000, step=1000)
    with col2:
        end_date = st.date_input("End date")
        style = st.selectbox("Travel style", ["balanced", "budget", "comfort", "family-friendly", "adventure"])
        interests = st.text_area("Interests", placeholder="History, food, markets, nature...", height=120)
    submitted = st.form_submit_button("Generate trip draft", type="primary", use_container_width=True)

if submitted:
    try:
        request = validate_request({
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "travelers": int(travelers),
            "budget_inr": int(budget),
            "interests": interests,
            "travel_style": style,
        })
        if (request.end_date - request.start_date).days > 30:
            raise ValueError("For this demo, please plan trips of 31 days or fewer.")
        st.session_state.request = request.model_dump(mode="json")
        st.session_state.approved = False
        with st.spinner("Agents are researching, building, budgeting, and reviewing your plan..."):
            result = create_trip_plan(st.session_state.request)
        st.session_state.draft = result["final_draft"]
        st.session_state.warnings = validate_draft(result["final_draft"], request.budget_inr)
    except Exception as e:
        st.error(f"Could not generate a trip plan: {e}")

if st.session_state.draft:
    st.divider()
    st.subheader("Proposed itinerary — human review required")
    for warning in st.session_state.warnings:
        st.warning(warning)
    st.markdown(st.session_state.draft)
    st.caption("Review the plan carefully. Costs and travel suggestions are AI-generated estimates, not verified live information.")

    st.subheader("Human-in-the-Loop")
    st.write("Approve the draft, or provide feedback and regenerate it before treating it as final.")
    feedback = st.text_area("Requested changes (optional)", placeholder="Example: reduce hotel cost and add a museum visit")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Approve itinerary", type="primary", use_container_width=True):
            st.session_state.approved = True
    with c2:
        if st.button("🔄 Revise with feedback", use_container_width=True):
            if not feedback.strip():
                st.warning("Please enter the changes you want.")
            else:
                req = dict(st.session_state.request)
                req["interests"] = f"{req['interests']}. Human feedback for revision: {feedback.strip()}"
                try:
                    checked = validate_request(req)
                    with st.spinner("Agents are revising your itinerary..."):
                        result = create_trip_plan(checked.model_dump(mode="json"))
                    st.session_state.request = checked.model_dump(mode="json")
                    st.session_state.draft = result["final_draft"]
                    st.session_state.warnings = validate_draft(result["final_draft"], checked.budget_inr)
                    st.session_state.approved = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Revision failed validation: {e}")

    if st.session_state.approved:
        st.success("Human approval recorded. This itinerary is marked as approved in this session.")
        st.download_button(
            "Download approved itinerary",
            data=st.session_state.draft,
            file_name="approved_trip_itinerary.md",
            mime="text/markdown",
            use_container_width=True,
        )
        st.caption("Approval is session-only in this starter project; no booking is made and no database persistence is configured.")

with st.expander("Guardrails in this demo"):
    st.markdown(
        "- **Input:** Pydantic validates field lengths, date order, traveler count, and budget bounds.\n"
        "- **Prompt-injection screening:** basic pattern checks reject a few instruction-override phrases.\n"
        "- **Output:** checks for a non-empty plan, estimate disclaimer, and INR cost information.\n"
        "- **Human review:** the plan is not marked approved until you click Approve.\n\n"
        "These are starter safeguards, not a complete security system. Add stronger moderation, source verification, "
        "structured output validation, logging, and tests before production use."
    )
