from flask import Flask, request, jsonify, render_template, url_for
from openai import OpenAI

app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # Get the user input from the form
    user_input = request.form['question']
    
    # Create the API request
    completion = client.chat.completions.create(
        model="writer/palmyra-med-70b",
        messages=[{"role": "user", "content": user_input}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )
    
    # Collect the response from the API
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
