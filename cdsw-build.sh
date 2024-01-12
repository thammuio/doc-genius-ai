echo "Building CDSW Model Serving Deps"

pip install -r requirements.txt

# Install Model Dependencies
sh session/install-deps/install_llama_deps.sh