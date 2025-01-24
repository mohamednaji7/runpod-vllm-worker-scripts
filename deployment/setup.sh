
# Exit on error
set -e

apt-get update 
apt-get install wget


# Define variables
CONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
CONDA_INSTALL_PATH="$HOME/miniconda3"
ENV_NAME="unsloth_env"

# Download Miniconda installer
if [ ! -f "$CONDA_INSTALLER" ]; then
    echo "Downloading Miniconda installer..."
    wget -q "https://repo.anaconda.com/miniconda/$CONDA_INSTALLER"
else
    echo "Miniconda installer already exists. Skipping download."
fi

# Install Miniconda silently
if [ ! -d "$CONDA_INSTALL_PATH" ]; then
    echo "Installing Miniconda..."
    bash "$CONDA_INSTALLER" -b -p "$CONDA_INSTALL_PATH"
else
    echo "Miniconda is already installed. Skipping installation."
fi

# Initialize Conda for bash
echo "Initializing Conda..."
"$CONDA_INSTALL_PATH/bin/conda" init bash

# Source Conda setup script directly for the current session
source "$CONDA_INSTALL_PATH/etc/profile.d/conda.sh"

# Create an empty Conda environment
echo "Creating an empty Conda environment: $ENV_NAME..."
# "$CONDA_INSTALL_PATH/bin/conda" create --name "$ENV_NAME" python=3.10 -y
"$CONDA_INSTALL_PATH/bin/conda" create --name "$ENV_NAME" --no-default-packages -y

# Activate the new environment for the current session
echo "Activating environment: $ENV_NAME..."
conda activate "$ENV_NAME"

# Verify Conda environment
echo "Environment created and activated successfully:"
conda info --envs

echo "Done! You can now use Conda and your environment."

# # Unsloth
# echo "Let's get Unsloth..."

# conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
# conda install xformers -c xformers -y

# pip install bitsandbytes
# pip install "unsloth[conda] @ git+https://github.com/unslothai/unsloth.git"

# echo "Done! You can now use Conda and Unsloth."

source ~/.bashrc
