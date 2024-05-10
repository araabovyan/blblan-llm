import re

from flask import Flask, request, Response
from llama_cpp import Llama

app = Flask(__name__)

# Initialize the Llama model
llm = Llama(model_path="./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", chat_format="llama-2", n_gpu_layers=35)

@app.route('/process_message', methods=['POST'])
def process_message():
    try:
        # Parse the incoming JSON data
        data = request.get_json()
        message_text = data['messageText']

        # Create the stream from the Llama model
        stream = llm.create_chat_completion(stream=False, messages=[
            {"role": "system", "content": "You are a chat bot with very short answers."},
            {"role": "user", "content": message_text}
        ])
        response = stream['choices'][0]['message']['content']
        response = response.replace('[/INST]', '')
        response = response.replace('[/SYS]', '')
        response = re.sub(r'\s+', ' ', response)

        print('=====================>>>>>>>>>')
        print(response)

        # Define a generator function to yield messages
        # def generate():
        #     for msg in stream:
        #         try:
        #             yield msg['choices'][0]['delta']['content'] + '\n'
        #         except KeyError:
        #             yield '\n'

        # Stream the response back to the client
        # return Response(generate(), mimetype='text/plain')
        return Response(response, mimetype='text/plain')
    
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
