# Guide 13: Scaling & Performance

## What This Does
Optimizes JanSeva to handle 100 concurrent users (test target) and architect for 1,000+ users (scale target).

## Prerequisites
- All Phase 1-3 guides completed
- System running end-to-end on Telegram

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Text query response time | < 5 seconds |
| Voice query response time | < 15 seconds |
| Concurrent users | 100 (test), 1,000 (scale) |
| Database queries per request | < 5 |
| Memory per bot process | < 512 MB |

---

## Optimization Areas

### 1. Database Connection Pooling
```python
# Already configured in engine.py — tune these values:
engine = create_async_engine(
    settings.database_url,
    pool_size=20,      # Increase from 10
    max_overflow=40,   # Increase from 20
    pool_pre_ping=True,
    pool_recycle=3600,  # Recycle connections every hour
)
```

### 2. Redis Response Caching
Cache common queries (e.g., "income certificate requirements") to avoid hitting the LLM for every identical question:

```python
import hashlib
import json
from redis.asyncio import Redis

async def get_cached_response(query: str, redis: Redis) -> str | None:
    key = f"response:{hashlib.sha256(query.lower().encode()).hexdigest()}"
    cached = await redis.get(key)
    return cached.decode() if cached else None

async def cache_response(query: str, response: str, redis: Redis, ttl: int = 3600):
    key = f"response:{hashlib.sha256(query.lower().encode()).hexdigest()}"
    await redis.setex(key, ttl, response)
```

### 3. Database Indexes
```sql
-- Add these indexes for query performance:
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_conversations_user_active ON conversations(user_id) WHERE status = 'active';
CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at DESC);
CREATE INDEX idx_reports_status ON anonymous_reports(status) WHERE status != 'resolved';
CREATE INDEX idx_escalated_status ON escalated_queries(status) WHERE status = 'pending';
```

### 4. Horizontal Scaling

Run multiple bot instances:
```bash
# Run 3 bot workers (each handles a slice of users)
docker compose up --scale bot=3
```

For Telegram polling: only ONE instance can poll. Use webhook mode for multiple workers:
```python
# Switch from polling to webhook mode:
# 1. Set up a webhook URL (requires HTTPS)
# 2. Telegram sends updates to your server
# 3. Multiple workers can process from a shared queue
```

### 5. Load Testing

Use `locust` to simulate 100 concurrent users:

```python
# tests/load/locustfile.py
from locust import HttpUser, task, between

class TelegramSimulator(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def send_message(self):
        self.client.post("/webhook", json={
            "update_id": 12345,
            "message": {
                "text": "आय प्रमाण पत्र कैसे बनाएं?",
                # ... Telegram update format
            }
        })
```

---

## Monitoring

### Health Check Endpoint
```python
@admin_app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "db": await check_db_connection(),
        "redis": await check_redis_connection(),
        "uptime": get_uptime(),
    }
```

### Structured Logging Metrics
- Request count per endpoint
- Response time percentiles (p50, p95, p99)
- Error rate
- Queue depth (pending escalations, unprocessed reports)

---

## Git Checkpoint
```bash
git add -A
git commit -m "perf(scale): optimize for 100 concurrent users

- Database connection pool tuning
- Redis response caching for common queries
- Database index optimization
- Health check endpoint
- Load testing setup with Locust"
```
