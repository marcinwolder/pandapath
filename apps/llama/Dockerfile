FROM python:3.11-slim

ARG MODEL_URL="https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_0.gguf"
ENV MODEL_URL=${MODEL_URL}
ENV MODEL_PATH=/models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf

ENV CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates build-essential cmake libopenblas-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "llama-cpp-python[server]==0.3.16"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

VOLUME ["/models"]
ENV LLAMA_CPP_MODEL_PATH=${MODEL_PATH}

ENTRYPOINT ["/entrypoint.sh"]
CMD ["--model", "/models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf", "--host", "0.0.0.0", "--port", "3000"]
