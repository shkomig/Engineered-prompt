"""Tests for database module."""
import sys
from pathlib import Path
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import PromptDatabase


def test_database_creation():
    """Test database creation."""
    # Use test database
    test_db = "sqlite:///./test_prompts.db"
    db = PromptDatabase(test_db)

    assert db is not None
    print("✓ Database creation test passed")

    # Cleanup
    if os.path.exists("test_prompts.db"):
        os.remove("test_prompts.db")


def test_save_and_retrieve():
    """Test saving and retrieving prompts."""
    test_db = "sqlite:///./test_prompts.db"
    db = PromptDatabase(test_db)

    # Save a prompt
    prompt_id = db.save_prompt(
        input_text="כתוב לי מכתב",
        detected_intent="formal_letter",
        generated_prompt="Test prompt content",
        detected_style="formal",
        metadata={"test": "data"}
    )

    assert prompt_id is not None
    print(f"✓ Save test passed: ID {prompt_id}")

    # Retrieve it
    retrieved = db.get_prompt_by_id(prompt_id)
    assert retrieved is not None
    assert retrieved["input_text"] == "כתוב לי מכתב"
    assert retrieved["detected_intent"] == "formal_letter"
    print("✓ Retrieve test passed")

    # Cleanup
    if os.path.exists("test_prompts.db"):
        os.remove("test_prompts.db")


def test_feedback():
    """Test feedback update."""
    test_db = "sqlite:///./test_prompts.db"
    db = PromptDatabase(test_db)

    # Save a prompt
    prompt_id = db.save_prompt(
        input_text="test",
        detected_intent="general",
        generated_prompt="test prompt"
    )

    # Update feedback
    success = db.update_feedback(prompt_id, "good", 5.0)
    assert success
    print("✓ Feedback update test passed")

    # Verify
    retrieved = db.get_prompt_by_id(prompt_id)
    assert retrieved["user_feedback"] == "good"
    assert retrieved["rating"] == 5.0
    print("✓ Feedback verification test passed")

    # Cleanup
    if os.path.exists("test_prompts.db"):
        os.remove("test_prompts.db")


def test_history():
    """Test retrieving history."""
    test_db = "sqlite:///./test_prompts.db"
    db = PromptDatabase(test_db)

    # Add multiple prompts
    for i in range(5):
        db.save_prompt(
            input_text=f"test {i}",
            detected_intent="general",
            generated_prompt=f"prompt {i}"
        )

    # Get history
    history = db.get_prompt_history(limit=10)
    assert len(history) == 5
    print(f"✓ History test passed: {len(history)} records")

    # Cleanup
    if os.path.exists("test_prompts.db"):
        os.remove("test_prompts.db")


if __name__ == "__main__":
    print("Running database tests...\n")

    test_database_creation()
    test_save_and_retrieve()
    test_feedback()
    test_history()

    print("\n✅ All tests passed!")
