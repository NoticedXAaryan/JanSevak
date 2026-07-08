"""
Escalation Agent — Handles queries the AI cannot answer.
Logs the query and routes it to the admin panel for human review.

Full implementation in Guide 06.
"""

import structlog

logger = structlog.get_logger()


def handle_escalation(state: dict) -> dict:
    """
    Handle queries that need human attention.

    Phase 1: Log and inform user.
    Phase 2 (Guide 06): Store in DB, notify admin, track resolution.
    """
    latest_message = state["messages"][-1].content if state["messages"] else "unknown"
    user_language = state.get("user_language", "hi")

    logger.warning(
        "query_escalated",
        query_preview=latest_message[:100],
        reason="ai_cannot_answer",
    )

    response = (
        "🔄 <b>आपका सवाल हमारी टीम को भेज दिया गया है।</b>\n\n"
        "यह सवाल हमारे AI के दायरे से बाहर है। हमारी प्रशासनिक टीम "
        "इसकी जाँच करेगी और जल्द से जल्द आपको जवाब देगी।\n\n"
        "📝 आपका सवाल दर्ज कर लिया गया है। आपको अपडेट मिलेगा।\n\n"
        "<i>Your query has been forwarded to our team. "
        "They will review it and get back to you soon.</i>"
    )

    return {
        "response": response,
        "needs_escalation": True,
        "escalation_reason": "AI could not provide a confident answer",
    }
