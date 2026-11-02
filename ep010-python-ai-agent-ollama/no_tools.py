from ollama import chat
r = chat(model="qwen2.5-coder:3b", messages=[{"role": "user", "content": "What is today's date? Answer in one line."}])
print(r.message.content)
