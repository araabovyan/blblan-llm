# blblan-llm


## Installation

### Step 1: Install Requirements

First, you need to install the necessary Python packages. Open your terminal and execute the following command:

```bash
pip install -r requirements.txt
```

Run one of the following commands according to your system

```bash
# Base ctransformers with no GPU acceleration
pip install llama-cpp-python
# With NVidia CUDA acceleration
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
# Or with OpenBLAS acceleration
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python
# Or with CLBLast acceleration
CMAKE_ARGS="-DLLAMA_CLBLAST=on" pip install llama-cpp-python
# Or with AMD ROCm GPU acceleration (Linux only)
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" pip install llama-cpp-python
# Or with Metal GPU acceleration for macOS systems only
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

# In windows, to set the variables CMAKE_ARGS in PowerShell, follow this format; eg for NVidia CUDA:
$env:CMAKE_ARGS = "-DLLAMA_OPENBLAS=on"
pip install llama-cpp-python
```

### Step 2: Download the model

Next, you need to download the required model using the Hugging Face CLI

```bash
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --local-dir ./models/ --local-dir-use-symlinks False
huggingface-cli download TheBloke/Llama-2-7B-Chat-GGUF llama-2-7b-chat.Q3_K_M.gguf --local-dir ./models/ --local-dir-use-symlinks False
```

## Usage

### Running the Application

To start the application, navigate to the project directory and run `app.py` by executing:

```bash
python app.py
```
This will start the Flask application, and it should be accessible via `http://localhost:5000` on your browser.


### Making API Calls

For small mdoel

```bash
curl -X POST http://localhost:5000/process_message1 \
-H "Content-Type: application/json" \
-d '{"userID": "123", "conversationID": "456", "messageText": "Hello, how are you?"}'
```

For big mdoel

```bash
curl -X POST http://localhost:5000/process_message2 \
-H "Content-Type: application/json" \
-d '{"userID": "123", "conversationID": "456", "messageText": "Hello, how are you?"}'
```
