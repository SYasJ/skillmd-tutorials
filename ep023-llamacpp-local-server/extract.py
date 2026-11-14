import json
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:9931/v1", api_key="not-needed")

schema = {"type": "object",
          "properties": {"name": {"type": "string"}, "date": {"type": "string"}, "time": {"type": "string"}},
          "required": ["name", "date", "time"]}

reply = client.chat.completions.create(
    model="local",
    messages=[{"role": "user", "content": "Book a table for Maria on Friday Nov 20 at 7:30 pm, please."}],
    response_format={"type": "json_schema", "json_schema": {"name": "booking", "schema": schema}},
    extra_body={"chat_template_kwargs": {"enable_thinking": False}},
)
data = json.loads(reply.choices[0].message.content)
print(data)
print("name ->", data["name"])
