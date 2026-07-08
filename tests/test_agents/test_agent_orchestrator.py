from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from janseva.agents.orchestrator import classify_intent, route_by_intent
from janseva.agents.state import AgentState


@pytest.fixture
def mock_llm():
    with patch("janseva.agents.orchestrator.get_llm") as mock:
        llm_instance = MagicMock()
        mock.return_value = llm_instance
        yield llm_instance


def test_classify_intent_service_query(mock_llm):
    # Mock LLM to return "service_query"
    mock_llm.invoke.return_value = AIMessage(content="service_query")

    state = AgentState(
        messages=[HumanMessage(content="आय प्रमाण पत्र कैसे बनाएं?")],
        user_language="hi",
        user_district="bhopal",
    )

    result = classify_intent(state)
    assert result["intent"] == "service_query"


def test_classify_intent_fallback(mock_llm):
    # Mock LLM returning invalid intent
    mock_llm.invoke.return_value = AIMessage(content="some_random_stuff")

    state = AgentState(
        messages=[HumanMessage(content="Hello")],
    )

    result = classify_intent(state)
    assert result["intent"] == "general"  # Fallback behavior


def test_route_by_intent():
    assert route_by_intent({"intent": "service_query"}) == "service_navigator"
    assert route_by_intent({"intent": "anonymous_report"}) == "anonymous_report_node"
    assert route_by_intent({"intent": "unknown_value"}) == "general_chat"
