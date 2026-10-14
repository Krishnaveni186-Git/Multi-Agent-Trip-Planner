# ✈️ Multi-Agent Trip Planner with Guardrails and Human-in-the-Loop

**Agentic AI • Multi-Agent Systems • Responsible AI • Human-in-the-Loop • Streamlit**

An AI-powered trip planning application that uses multiple specialized AI agents to help users plan personalized trips. The system combines collaborative agent workflows, guardrails for safer AI responses, and Human-in-the-Loop (HITL) approval to improve the reliability and usability of AI-generated travel recommendations.

## 📌 Project Overview

Planning a trip involves multiple decisions, including destination selection, itinerary creation, accommodation, transportation, and budgeting. Managing these tasks manually can be time-consuming.

The **Multi-Agent Trip Planner** aims to simplify this process by coordinating specialized AI agents to generate travel recommendations based on user preferences, trip duration, budget, and destination.

The application integrates guardrails to validate relevant inputs and outputs, while Human-in-the-Loop functionality allows users to review and approve proposed plans before proceeding.

The application is developed in **VS Code** and presented through an interactive **Streamlit** web interface.

## 🎯 Project Objectives

- Automate trip planning using a multi-agent AI architecture.
- Generate personalized travel itineraries based on user requirements.
- Coordinate specialized agents for different planning tasks.
- Implement guardrails to improve the safety and quality of AI outputs.
- Introduce human approval checkpoints for greater user control.
- Provide an interactive interface for submitting preferences and reviewing trip plans.

## ✨ Key Features

- **Multi-Agent Architecture:** Divides trip-planning tasks among specialized AI agents.
- **Personalized Itinerary Generation:** Creates travel plans based on user-provided preferences.
- **Input Guardrails:** Helps validate user inputs before processing.
- **Output Guardrails:** Supports checking generated recommendations against defined rules.
- **Human-in-the-Loop:** Enables users to review, approve, or request changes to a proposed itinerary.
- **Interactive Streamlit UI:** Provides an accessible interface for trip-planning interactions.
- **Modular Development:** Organizes the application into components for easier maintenance and future enhancements.

## 🏗️ System Architecture

The application follows a multi-agent workflow in which the user's requirements are processed, delegated to specialized agents, validated, and presented for human review.

### Workflow

1. **User Input:** The user enters the destination, travel dates, budget, interests, and other trip preferences.
2. **Input Validation:** Guardrails check the provided information against configured validation rules.
3. **Agent Orchestration:** The orchestration layer coordinates the relevant AI agents.
4. **Trip Planning:** Specialized agents contribute travel recommendations and itinerary details.
5. **Output Validation:** Generated results are checked against the configured guardrails.
6. **Human Review:** The user reviews the proposed itinerary and approves it or requests modifications.
7. **Final Output:** The application presents the reviewed trip plan.

## 🛠️ Technology Stack

**Technology**                       **Purpose** 

- Python                          Core application development 
- Streamlit                       Interactive web application 
- Multi-Agent Framework           Agent coordination and task execution
- Large Language Models (LLMs)    Natural-language reasoning and itinerary generation
- Guardrails                      Input and output validation
- Human-in-the-Loop               User review and approval
- Visual Studio Code              Development environment

*Update the framework and model entries with the exact libraries and providers used in your project.*

## 📂 Project Structure

A possible project structure is shown below. Update it to match your repository.

```text
Multi-Agent-Trip-Planner/
│
├── Backend/
│   ├── agents.py
│   ├── guardrails.py
│   └── ...
│
├── frontend/
│   └── app.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md

## 🛡️ **Guardrails and Responsible AI**

Guardrails help establish boundaries around AI-generated recommendations and user inputs.

Potential safeguards include:

- **Input Validation:** Check required fields and reject invalid values.
- **Constraint Validation:** Check whether recommendations align with the user's stated budget, dates, and preferences.
- **Output Validation:** Check generated responses for missing information or violations of configured rules.
- **Error Handling:** Handle incomplete responses and model or API failures gracefully.
- **Human Oversight:** Require review before accepting a proposed itinerary where approval is configured.

Guardrails can reduce avoidable errors, but they do not guarantee that every recommendation is accurate. Travel details such as prices, availability, visa requirements, and opening hours should be independently verified.

## 👤 Human-in-the-Loop (HITL)

Human-in-the-Loop introduces a user review step into the AI workflow.

**Typical approval flow:**

- **Generate:** AI agents create a proposed trip plan.
- **Validate:** Configured guardrails evaluate the generated content.
- **Review:** The user inspects the itinerary and any warnings.
- **Decide:** The user approves the plan or requests changes.
- **Refine:** The system regenerates or updates the proposal when supported.

This approach keeps the user involved in important decisions instead of relying entirely on automated AI output.

## 🔄 Complete Project Workflow

Multi-Agent Trip Planner Workflow

The workflow illustrates how user preferences pass through input guardrails,
specialized AI agents, output validation, and human review before producing
the final trip itinerary.

**Project Focus:** Agentic AI | Multi-Agent Systems | LLM Guardrails | Human-in-the-Loop | Responsible AI | Streamlit


<img width="1228" height="819" alt="Trip Planner Workflow" src="https://github.com/user-attachments/assets/426af478-8113-42de-8683-5b66ebbd9349" />


