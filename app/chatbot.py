from openai import OpenAI
client = OpenAI()


def get_response(prompt):
    prompt_message = [{"role": "system", "content": prompt}]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt_message
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content
