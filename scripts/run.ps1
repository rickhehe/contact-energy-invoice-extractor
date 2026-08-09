# PowerShell script to run the app using uv, which manages the venv and dependencies automatically

# Ensure uv is available
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv not found. Install it from https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
}

# Sync the environment with pyproject.toml/uv.lock (creates .venv and installs dependencies as needed)
uv sync

# Run the app
uv run python -m src.main
