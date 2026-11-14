from openai import OpenAI

# same SDK you use for OpenAI - only the address changes
client = OpenAI(base_url="http://127.0.0.1:9931/v1", api_key="not-needed")

reply = client.chat.completions.create(
    model="local",
    messages=[{"role": "user", "content": "Explain llama.cpp to a 10-year-old in 2 sentences."}],
    extra_body={"chat_template_kwargs": {"enable_thinking": False}},
)
print(reply.choices[0].message.content)
