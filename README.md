# blblan-llm


## Installation

### Step 1: Install Requirements

First, you need to install the necessary Python packages. Open your terminal and execute the following command:

```bash
pip install -r requirements.txt
```

### Step 2: Install Requirements

Next, you need to download the required model using the Hugging Face CLI

```bash
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --local-dir .models/ --local-dir-use-symlinks False
```

## Usage

### Running the Application

To start the application, navigate to the project directory and run `app.py` by executing:

```bash
python app.py
```
This will start the Flask application, and it should be accessible via `http://localhost:5000` on your browser.


### Making API Calls

```bash
curl -X POST http://localhost:5000/process_message \
-H "Content-Type: application/json" \
-d '{"userID": "123", "conversationID": "456", "messageText": "Hello, how are you?"}'
```
