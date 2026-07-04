import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import Message, User, Chat

from janseva.bot.routers.text import handle_text_message

@pytest.fixture
def mock_message():
    msg = MagicMock(spec=Message)
    msg.text = "Hello JanSeva"
    msg.from_user = MagicMock(spec=User)
    msg.from_user.id = 123456789
    msg.chat = MagicMock(spec=Chat)
    msg.chat.id = 123456789
    
    # Async mock for edit_text and answer
    msg.answer = AsyncMock()
    msg.edit_text = AsyncMock()
    return msg

@pytest.mark.asyncio
@patch("janseva.bot.routers.text.async_session_factory")
@patch("janseva.bot.routers.text.process_message")
@patch("janseva.bot.routers.text.send_thinking")
@patch("janseva.bot.routers.text.update_with_response")
async def test_handle_text_message_success(
    mock_update, 
    mock_thinking, 
    mock_process, 
    mock_session_factory, 
    mock_message
):
    # Setup mocks
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    
    # Mock user query result
    mock_result = MagicMock()
    mock_db_user = MagicMock()
    mock_db_user.onboarding_complete = True
    mock_result.scalar_one_or_none.return_value = mock_db_user
    mock_session.execute.return_value = mock_result
    
    # Mock thinking and processing
    thinking_msg = MagicMock(spec=Message)
    mock_thinking.return_value = thinking_msg
    mock_process.return_value = "This is a response"
    
    await handle_text_message(mock_message)
    
    # Verify calls
    mock_thinking.assert_called_once_with(mock_message)
    mock_process.assert_called_once_with(
        telegram_id=123456789,
        user_text="Hello JanSeva"
    )
    mock_update.assert_called_once_with(mock_message, thinking_msg, "This is a response")

@pytest.mark.asyncio
@patch("janseva.bot.routers.text.async_session_factory")
@patch("janseva.bot.routers.start.handle_start")
async def test_handle_text_message_unonboarded(
    mock_handle_start, 
    mock_session_factory, 
    mock_message
):
    # Setup mocks
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    
    # Mock user query result - user not found (or not onboarded)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result
    
    await handle_text_message(mock_message)
    
    # Verify it redirects to start
    mock_handle_start.assert_called_once_with(mock_message)
