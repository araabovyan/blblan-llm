import re
import json
import os

from flask import Flask, request, Response
from llama_cpp import Llama

app = Flask(__name__)

# Initialize the Llama model
llm = Llama(model_path="./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", chat_format="llama-2", n_gpu_layers=35, verbose=False)

def get_history(user_id, conversation_id, message_length, max_length=1500):
    """ Retrieve messages from history if available """
    filename = f"{user_id}_{conversation_id}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            history = json.load(file)
        while len(str(history)) + message_length > max_length:
            history.pop(0)
        return history
    return []

def save_history(user_id, conversation_id, messages):
    """ Save the updated conversation history """
    filename = f"{user_id}_{conversation_id}.json"
    with open(filename, 'w') as file:
        json.dump(messages, file)


@app.route('/process_message', methods=['POST'])
def process_message():
    try:
        # Parse the incoming JSON data
        data = request.get_json()
        user_id = data['userID']
        conversation_id = data['conversationID']
        message_text = data['messageText']
        use_stream = data.get('stream', False)

        # Retrieve or initialize conversation history
        history = get_history(user_id, conversation_id, len(message_text))
        history.append({"role": "user", "content": message_text})

        print(history)
        # Create the stream from the Llama model
        stream = llm.create_chat_completion(stream=use_stream, messages=[
            {"role": "system", "content": "You are a chat bot with very short answers."}
        ] + history)
        if use_stream:
            # Define a generator function to yield messages
            def generate():
                for msg in stream:
                    try:
                        yield msg['choices'][0]['delta']['content'] + '\n'
                    except KeyError:
                        yield '\n'
                    # Stream the response back to the client
            return Response(generate(), mimetype='text/plain')
        else:
            response = stream['choices'][0]['message']['content']
            response = response.replace('[INST]', '')
            response = response.replace('[/INST]', '')
            response = response.replace('<<INST>', '')
            response = response.replace('<</INST>', '')
            response = response.replace('[SYS]', '')
            response = response.replace('[/SYS]', '')
            response = response.replace('<<SYS>>', '')
            response = response.replace('<</SYS>>', '')
            response = response.replace('<|assistant|>', '')
            response = response.replace('<|user|>', '')
            response = response.replace('\ufffc', '')
            response = re.sub(r'\s+', ' ', response)
            return Response(response, mimetype='text/plain')

    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
