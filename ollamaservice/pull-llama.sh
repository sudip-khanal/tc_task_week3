
# Start Ollama service in the background
./bin/ollama serve &

# Capture the PID of the background process
pid=$!

# Wait for the service to initialize
sleep 10  # Increased wait time for initialization

# Print a message indicating the model is being pulled
echo "Pulling llama qwen2 model"

# Pull the model
ollama pull qwen2:0.5b

# Optionally wait for the process to finish (if needed)
wait $pid
