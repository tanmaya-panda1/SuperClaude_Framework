"""Unit tests for SuperClaude CLI command wiring."""

from click.testing import CliRunner

from superclaude.cli.main import main


def test_cli_help_shows_core_commands():
    """CLI help should include key commands."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "install" in result.output
    assert "mcp" in result.output
    assert "doctor" in result.output
    assert "version" in result.output


def test_cli_version_command():
    """Version command should return version text."""
    runner = CliRunner()
    result = runner.invoke(main, ["version"])

    assert result.exit_code == 0
    assert "SuperClaude version" in result.output


def test_install_list_command(monkeypatch):
    """Install --list should print available commands and agents."""
    runner = CliRunner()

    monkeypatch.setattr(
        "superclaude.cli.install_commands.list_available_commands",
        lambda: ["research", "test"],
    )
    monkeypatch.setattr(
        "superclaude.cli.install_commands.list_installed_commands",
        lambda: ["research"],
    )
    monkeypatch.setattr(
        "superclaude.cli.install_commands.list_available_agents",
        lambda: ["pm-agent"],
    )

    result = runner.invoke(main, ["install", "--list"])

    assert result.exit_code == 0
    assert "/research" in result.output
    assert "@pm-agent" in result.output


def test_mcp_list_command(monkeypatch):
    """MCP --list should execute list function."""
    runner = CliRunner()

    monkeypatch.setattr(
        "superclaude.cli.install_mcp.list_available_servers",
        lambda: None,
    )

    result = runner.invoke(main, ["mcp", "--list"])

    assert result.exit_code == 0


def test_mcp_list_command_without_claude_binary(monkeypatch):
    """MCP --list should not crash if Claude CLI is not installed."""
    runner = CliRunner()

    monkeypatch.setattr(
        "superclaude.cli.install_mcp._run_command",
        lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError()),
    )

    result = runner.invoke(main, ["mcp", "--list"])

    assert result.exit_code == 0
    assert "Available MCP Servers" in result.output


def test_doctor_success(monkeypatch):
    """Doctor should exit successfully when all checks pass."""
    runner = CliRunner()

    monkeypatch.setattr(
        "superclaude.cli.doctor.run_doctor",
        lambda verbose=False: {
            "checks": [
                {"name": "pytest plugin loaded", "passed": True, "details": []},
                {"name": "Skills installed", "passed": True, "details": []},
                {"name": "Configuration", "passed": True, "details": []},
            ]
        },
    )

    result = runner.invoke(main, ["doctor"])

    assert result.exit_code == 0
    assert "SuperClaude is healthy" in result.output


def test_doctor_failure(monkeypatch):
    """Doctor should return non-zero when any check fails."""
    runner = CliRunner()

    monkeypatch.setattr(
        "superclaude.cli.doctor.run_doctor",
        lambda verbose=False: {
            "checks": [
                {"name": "pytest plugin loaded", "passed": False, "details": []},
                {"name": "Skills installed", "passed": True, "details": []},
                {"name": "Configuration", "passed": True, "details": []},
            ]
        },
    )

    result = runner.invoke(main, ["doctor"])

    assert result.exit_code == 1
    assert "checks failed" in result.output
