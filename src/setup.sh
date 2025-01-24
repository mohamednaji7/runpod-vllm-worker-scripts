apt-get update 
apt-get install wget

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b

~/miniconda3/bin/conda init
source ~/.bashrc


conda create --name unsloth_env python=3.10 -y

conda activate unsloth_env  

conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
conda install xformers -c xformers -y

pip install bitsandbytes
pip install "unsloth[conda] @ git+https://github.com/unslothai/unsloth.git"