import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

load_dotenv(override = True)

class TripState(TypedDict, total=False):
    request: dict
    research: str
    itinerary: str
    budget_review: str
    final_draft: str
    warnings: list[str]

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GORQ_API_KEY is missing. Add it to your .env file.")
    model = os.getenv("GORQ_MODEL", "openai/gpt-oss-120b")
    return ChatGroq(model=model, temperature=0.3, api_key=api_key)

def ask(system: str, user: str) -> str:
    response = get_llm().invoke([
        SystemMessage(content=system),
        HumanMessage(content=user),
    ])
    return str(response.content)

def research_agent(state: TripState):
    r = state["request"]
    prompt = f"""Research-planning task for a travel assistant.
Destination: {r['destination']}
Dates: {r['start_date']} to {r['end_date']}
Travelers: {r['travelers']}
Interests: {r['interests']}
Travel style: {r['travel_style']}

Suggest attractions and activities grouped by area where practical. Mention practical travel considerations.
Do not claim you checked live availability, opening hours, weather, or current prices. Clearly label uncertain facts and suggest verifying them from official sources."""
    result = ask("You are the Destination Research Agent. Be helpful, cautious, and concise.", prompt)
    return {"research": result}

def itinerary_agent(state: TripState):
    r = state["request"]
    prompt = f"""Create a day-by-day itinerary using the destination research below.
Trip: {r['destination']}; dates {r['start_date']} through {r['end_date']}; {r['travelers']} traveler(s);
budget ceiling ₹{r['budget_inr']}; interests: {r['interests']}; style: {r['travel_style']}.
Number of days should match the date range, counting both start and end dates.
Keep the schedule realistic, include meal/rest breaks, and avoid pretending bookings have been made.
Destination research:
{state['research']}"""
    result = ask("You are the Itinerary Agent. Structure the answer with headings for each day.", prompt)
    return {"itinerary": result}

def budget_agent(state: TripState):
    r = state["request"]
    prompt = f"""Estimate trip costs in INR for {r['destination']} for {r['travelers']} traveler(s),
from {r['start_date']} to {r['end_date']}, budget ceiling ₹{r['budget_inr']}.
Itinerary:
{state['itinerary']}

Provide a transparent table with categories such as local transport, food, activities, accommodation,
and intercity transport only if applicable. State assumptions, show an approximate total, and say what is
excluded. Do not invent live quotes. Explicitly say prices are estimates and must be checked before booking.
If the budget is tight, recommend specific ways to reduce cost."""
    result = ask("You are the Budget Agent. Do arithmetic carefully and flag uncertainty.", prompt)
    return {"budget_review": result}

def review_agent(state: TripState):
    r = state["request"]
    prompt = f"""Review this proposed trip for contradictions, missing details, unrealistic pacing, and budget risk.
Budget ceiling: ₹{r['budget_inr']}. Travelers: {r['travelers']}.
Research:
{state['research']}
Itinerary:
{state['itinerary']}
Budget estimate:
{state['budget_review']}

Return: (1) important issues, (2) corrections/recommendations, (3) a concise final draft with itinerary and budget.
Do not claim live verification or bookings. Clearly mark all costs as estimates."""
    result = ask("You are the Travel Plan Review Agent. Be skeptical and do not invent verification.", prompt)
    return {"final_draft": result}

def build_graph():
    graph = StateGraph(TripState)
    graph.add_node("research", research_agent)
    graph.add_node("itinerary", itinerary_agent)
    graph.add_node("budget", budget_agent)
    graph.add_node("review", review_agent)
    
    graph.add_edge(START, "research")
    graph.add_edge("research", "itinerary")
    graph.add_edge("itinerary", "budget")
    graph.add_edge("budget", "review")
    graph.add_edge("review", END)
    return graph.compile()

def create_trip_plan(request: dict) -> dict:
    return build_graph().invoke({"request": request})
