import pytest
from unittest.mock import patch
from src.cli import main

def test_cli_main_execution(capsys):
    """Target lines 8, 10-14, 16, 52: CLI entry point and argument parsing paths."""
    
    # Test CLI execution with default or help arguments
    test_args = ["cli.py", "--help"]
    with patch("sys.argv", test_args):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    # Test CLI subcommand execution path (e.g., running screener via CLI)
    test_args_run = ["cli.py", "run", "--config", "default"]
    with patch("sys.argv", test_args_run), \
         patch("src.cli.run_pipeline") as mock_pipeline:
        mock_pipeline.return_value = 0
        
        # Invoke CLI entry point
        try:
            main()
        except SystemExit as e:
            assert e.code == 0
            
        assert mock_pipeline.called