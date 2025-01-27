#activate_UnslothEnv_run_handler.sh

# Exit on error
set -e


# Define variables
CONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
# CONDA_INSTALL_PATH="$HOME/miniconda3"
CONDA_INSTALL_PATH="$(pwd)/miniconda3"
ENV_NAME="unsloth_env"



# Initialize Conda for bash
echo "Initializing Conda..."
"$CONDA_INSTALL_PATH/bin/conda" init bash

# Source Conda setup script directly for the current session
source "$CONDA_INSTALL_PATH/etc/profile.d/conda.sh"


# Activate the new environment for the current session
echo "Activating environment: $ENV_NAME..."
conda activate "$ENV_NAME"


echo ""
echo "running `python3 unsloth_model.py`..."
echo ""
python3 unsloth_model.py

