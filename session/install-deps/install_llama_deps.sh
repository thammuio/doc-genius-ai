#!/bin/bash

# Get raw nvcc output
# RAW_NVCC_OUTPUT=$(/usr/local/cuda/bin/nvcc --version)
# echo "NVCC Output: $RAW_NVCC_OUTPUT"

# # Filter the line that contains the release version and extract the full CUDA version
# FILTERED_NVCC_OUTPUT=$(echo "$RAW_NVCC_OUTPUT" | grep "release")
# FULL_CUDA_VERSION=$(echo "$FILTERED_NVCC_OUTPUT" | awk '{print $6}' | cut -c2-)
# echo "Full CUDA Version: $FULL_CUDA_VERSION"

# # Construct CMAKE_CUDA_COMPILER path
# CMAKE_CUDA_COMPILER="/usr/local/cuda/bin/nvcc"
# export CMAKE_CUDA_COMPILER

# # Print it out for verification
# echo "Setting CMAKE_CUDA_COMPILER to $CMAKE_CUDA_COMPILER"

# export CUDACXX=$CMAKE_CUDA_COMPILER
# export CMAKE_ARGS="-DLLAMA_CUBLAS=on -DCMAKE_CUDA_ARCHITECTURES=native"
# export FORCE_CMAKE=1

## Build llama-cpp-python w/ CUDA enablement
pip install --no-cache-dir llama-cpp-python