import re
import json
import os

from flask import Flask, request, Response
from llama_cpp import Llama

app = Flask(__name__)

def initialize_llama(model_path):
    """ Helper to initialize Llama model """
    return Llama(model_path=model_path, chat_format="llama-2", n_gpu_layers=-1, verbose=False)

# Initialize different models for different endpoints
model1 = initialize_llama("./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
model2 = initialize_llama("./models/llama-2-7b-chat.Q3_K_M.gguf")

def get_history(user_id, conversation_id):
    """ Retrieve messages from history if available """
    filename = f"{user_id}_{conversation_id}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            history = json.load(file)
        return history
    return []

def save_history(user_id, conversation_id, messages):
    """ Save the updated conversation history """
    filename = f"{user_id}_{conversation_id}.json"
    with open(filename, 'w') as file:
        json.dump(messages, file)

def process_request(data, model):
    """ Process the POST request using specified Llama model """
    user_id = data['userID']
    conversation_id = data['conversationID']
    message_text = data['messageText']
    use_stream = data.get('stream', False)

    # Retrieve or initialize conversation history
    history = get_history(user_id, conversation_id)
    user_message = {"role": "user", "content": message_text}
    history.append(user_message)

    # Create the stream from the Llama model
    stream = model.create_chat_completion(stream=use_stream, messages=[
        {"role": "system", "content": "You are a chat bot with very short answers."}
    ] + history)

    response_content = generate_response_content(stream, use_stream)
    model_response = {"role": "model", "content": response_content}
    history.append(model_response)

    # Save the updated history including the model response
    save_history(user_id, conversation_id, history)

    return response_content, use_stream

@app.route('/process_message1', methods=['POST'])
def process_message_model1():
    try:
        data = request.get_json()
        response_content, use_stream = process_request(data, model1)
        return generate_final_response(response_content, use_stream)
    except Exception as e:
        return str(e), 400

@app.route('/process_message2', methods=['POST'])
def process_message_model2():
    try:
        data = request.get_json()
        response_content, use_stream = process_request(data, model2)
        return generate_final_response(response_content, use_stream)
    except Exception as e:
        return str(e), 400

def generate_response_content(stream, use_stream):
    """ Generate content from the model stream """
    if use_stream:
        response = ""
        for msg in stream:
            try:
                response += msg['choices'][0]['delta']['content'] + '\n'
            except KeyError:
                response += '\n'
        return response
    else:
        response = stream['choices'][0]['message']['content']
        # Clean the response
        response = clean_response(response)
        return response

def generate_final_response(response_content, use_stream):
    """ Generate the final HTTP response """
    if use_stream:
        def generate():
            yield response_content
        return Response(generate(), mimetype='text/plain')
    else:
        return Response(response_content, mimetype='text/plain')

def clean_response(response):
    """ Function to clean and format the response from the model """
    clean_tokens = ['[INST]', '[/INST]', '<<INST>', '<</INST>', '[SYS]', '[/SYS]', '<<SYS>>', '<</SYS>>', '', '\ufffc']
    for token in clean_tokens:
        response = response.replace(token, '')
    response = re.sub(r'\s+', ' ', response)
    return response


if __name__ == '__main__':
    app.run(debug=False, port=5000)
