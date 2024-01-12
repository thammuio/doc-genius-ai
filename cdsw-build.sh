# Install General Dependencies
echo "Building CDSW Model Serving Deps"
pip install -r requirements.txt

# Install LLM Model Dependencies
echo "Building LLM Model Deps"
sh session/install-deps/install_llama_deps.sh