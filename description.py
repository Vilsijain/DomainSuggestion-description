import asyncio
import aiohttp
from flask import Flask, request, jsonify
import openai
import os
from functools import lru_cache

app = Flask(__name__)
openai.api_key = 'API_kEY'


@lru_cache(maxsize=128)
async def generate_domain_suggestions_async(business_description):
    # Define your prompt to ChatGPT
    prompt = f"Generate 10 unique domain names related to a business with the description: '{business_description}' and with different TLDs: 'com', 'info', 'net', 'org', 'co', 'me', without using 'business.tld' format."

    # Generate a response from ChatGPT
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1000,
        n=10,  # Number of suggestions to generate
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Extract the generated suggestions from the response
    suggestions = response.choices[0].text.strip().split('\n')

    # Remove numbering from suggestions
    suggestions = [suggestion.split('. ', 1)[1] for suggestion in suggestions]

    return suggestions


@app.route('/suggest', methods=['POST'])
async def suggest_domain_names():
    data = await request.get_json()

    # Extract the business description from the request data
    business_description = data['business_description']

    # Use asyncio.gather to run multiple requests concurrently
    tasks = [generate_domain_suggestions_async(business_description) for _ in range(10)]
    suggestions = await asyncio.gather(*tasks)

    # Return the suggestions as a JSON response
    return jsonify(suggestions)


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 5000)))
