"""
LangGraph state definitions.
State is the data that flows through the agent graph.
Every node reads and updates this shared state.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """
    Shared state for the JanSeva agent graph.

    Fields:
        messages: Full conversation history (LangChain message format).
                  Uses `add_messages` reducer to append, not replace.
        user_language: Detected language of the user (e.g., 'hi', 'en', 'mr').
        user_district: User's district/location for localized results.
        user_telegram_id: Telegram user ID for DB lookups.
        intent: Classified intent from the orchestrator.
        response: Final text response to send back to the user.
        needs_escalation: Whether the query should be escalated to admin.
        escalation_reason: Why the query was escalated.
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_language: str
    user_district: str
    user_telegram_id: int
    intent: str
    location_context: str
    response: str
    interactive_options: list[dict]
    needs_escalation: bool
    escalation_reason: str
