from flask import Flask, request, jsonify
import re
import random
import openai

app = Flask(__name__)

# Configure OpenAI API credentials
openai.api_key = 'API_KEY'

# List of desired TLDs
tlds = ['com', 'info', 'net', 'org', 'co', 'me']

@app.route('/business-names', methods=['POST'])
def generate_business_names():
    # Get the request data
    data = request.get_json()
    
    # Extract description and location from the request
    description = data.get('description', '')
    location = data.get('location', '')
    
    # Generate business name suggestions using ChatGPT API
    prompt = f"Generate 10 business name ideas for a {description} in {location}"
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=10,  # Generate 10 tokens for each suggestion
        n=10  # Generate 10 suggestions
    )
    
    # Extract and format the generated suggestions
    raw_suggestions = [re.sub(r'\d+\.\s+', '', choice['text'].strip()) for choice in response.choices]
    
    # Add random TLDs to each suggestion
    suggestions = [f"{name}.{random.choice(tlds)}" for name in raw_suggestions]
    
    # Return the suggestions as a JSON response
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
