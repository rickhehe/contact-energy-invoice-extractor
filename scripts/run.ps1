# PowerShell script to run app.py with venv and requirements.txt checks using 'snake'

# Set variables
$venv_path = "./.venv"
$requirements = "./requirements.txt"

# Check for venv, create if missing
if (!(Test-Path $venv_path)) {
    Write-Host "Virtual environment not found. Creating venv..."
    python -m venv $venv_path
}

# Activate venv
$activate_script = Join-Path $venv_path "Scripts/Activate.ps1"
. $activate_script

# Check for requirements.txt and install if present
if (Test-Path $requirements) {
    Write-Host "Installing dependencies from requirements.txt..."
    python -m pip install -r $requirements | Out-Null
} else {
    Write-Host "requirements.txt not found. Skipping dependency installation."
}

# Run the app
python -m src.main

# Deactivate the virtual environment
deactivate
