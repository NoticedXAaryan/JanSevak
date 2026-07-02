# Guide 06: Query Escalation System

## What This Does
Handles queries the AI cannot answer by logging them and routing to the admin panel. Administrators review, respond, and the response is delivered back to the user via Telegram.

## Prerequisites
- Guide 03 completed (AI agent core)
- Guide 07 completed (admin dashboard — so admins can see and respond to escalations)

---

## Overview

When the AI detects a query it cannot confidently answer:
1. The query is stored in `escalated_queries` table with status `pending`
2. The user gets a message: "Your query has been forwarded to our team"
3. Admin dashboard shows the new escalation with the original question
4. Admin assigns it to a department, writes a response
5. The response is sent back to the user via Telegram bot

---

## Database Model

**File: `src/janseva/db/models/escalated_query.py`**

```python
"""Escalated query model — queries the AI couldn't answer, forwarded to humans."""
import uuid
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from janseva.db.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class EscalatedQuery(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "escalated_queries"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    original_query: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="uncategorized", nullable=False)
    department: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    # Statuses: pending, assigned, in_progress, responded, closed
    admin_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    assigned_to: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    user = relationship("User", lazy="selectin")
```

## Implementation Steps

1. Create the migration for `escalated_queries`
2. Update the escalation specialist agent to store queries in DB
3. Build an ARQ background job that checks for admin responses and sends them to users
4. Integrate with the admin dashboard (Guide 07)

## Key Code: Updated Escalation Agent

The escalation specialist in `src/janseva/agents/specialists/escalation.py` should:
- Use the LLM to categorize the query (which department?)
- Store it in `escalated_queries` with the user's ID
- Return a confirmation message with a reference number

## Key Code: Response Delivery Worker

Create `src/janseva/notifications/escalation_worker.py`:
- Polls `escalated_queries` for rows where `status = 'responded'` and admin_response is not null
- Sends the response to the user via Telegram bot
- Updates status to `closed`

---

## Git Checkpoint

```bash
git add -A
git commit -m "feat(escalation): implement query escalation to admin panel"
```
