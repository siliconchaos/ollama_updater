import pytest

from ollama_updater.main import check_dependencies, get_installed_models


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    import asyncio

    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_get_installed_models():
    """Test getting installed models."""
    models = await get_installed_models()
    assert isinstance(models, list)
    # Models should be strings if any exist
    assert all(isinstance(model, str) for model in models)


def test_check_dependencies():
    """Test dependency checking."""
    result = check_dependencies()
    assert isinstance(result, bool)


@pytest.mark.asyncio
async def test_get_installed_models_error_handling():
    """Test error handling in get_installed_models."""
    # This test assumes ollama is not installed or accessible
    # You might need to modify this based on your testing environment
    import asyncio
    import subprocess

    # Mock subprocess.create_subprocess_exec to simulate an error
    async def mock_create_subprocess_exec(*args, **kwargs):
        raise subprocess.SubprocessError("Mock error")

    # Save original function
    original_func = asyncio.create_subprocess_exec

    try:
        # Replace with mock
        asyncio.create_subprocess_exec = mock_create_subprocess_exec
        models = await get_installed_models()
        assert models == []  # Should return empty list on error
    finally:
        # Restore original function
        asyncio.create_subprocess_exec = original_func
