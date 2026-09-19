#!/usr/bin/env bash

set -e

echo "Creating or updating the AAI4323 Conda environment..."

conda env update \
    --name aai4323 \
    --file aai4323_conda_all.yml \
    --prune

echo "Checking the environment..."

conda run --name aai4323 python --version
conda run --name aai4323 python -m pip check

echo "Registering the Jupyter kernel..."

conda run --name aai4323 python -m ipykernel install \
    --user \
    --name aai4323 \
    --display-name "Python (AAI4323)"

echo "AAI4323 environment setup completed successfully."

echo "Configuring Conda for new terminals..."

conda init bash

grep -qxF "conda activate aai4323" ~/.bashrc || \
    echo "conda activate aai4323" >> ~/.bashrc

echo "New terminals will automatically activate the aai4323 environment."