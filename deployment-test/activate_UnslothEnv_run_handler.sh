# activate_UnslothEnv_run_handler.sh

# Exit on error
set -e



# Define variables
CONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
CONDA_INSTALL_PATH="/runpod-volume/miniconda3"
ENV_NAME="unsloth_env"

# Set environment variables for paths
export PATH="/runpod-volume/miniconda3/bin:$PATH"
export CONDA_ENVS_PATH="/runpod-volume/miniconda3/envs"
export PYTHONPATH="/runpod-volume"



# Initialize Conda for bash
echo "Initializing Conda..."
if ! "$CONDA_INSTALL_PATH/bin/conda" init bash; then
    echo "Failed to initialize Conda."
    exit 1
fi
# Source Conda setup script directly for the current session
source "$CONDA_INSTALL_PATH/etc/profile.d/conda.sh"


# Activate the new environment for the current session
if ! conda env list | grep -q "$ENV_NAME"; then
    echo "Environment $ENV_NAME does not exist. Please create it first."
    exit 1
fi
echo "Activating environment: $ENV_NAME..."
conda activate "$ENV_NAME"

echo "Python executable: $(which python)"
echo "Python version: $(python --version)"
echo "PYTHONPATH: $PYTHONPATH"
pip list | grep unsloth || echo "WARNING: unsloth is not installed in this environment."

echo ""
echo "running `python3 handler.py`..."
echo ""
python3 handler.py

