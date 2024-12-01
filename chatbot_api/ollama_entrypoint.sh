#!/bin/bash

/bin/ollama serve &

pid=$!

sleep 5

echo "Retrieve llama3.2 model..."
ollama pull llama3.2
echo "Done!"

wait $pid