import whisper

model = whisper.load_model("small")
result = model.transcribe("clip.mp3", language="en", fp16=False,
                          initial_prompt="Claude Code, Ollama, Gemma 4")

for seg in result["segments"]:
    print(f'{seg["start"]:6.1f}s  {seg["text"].strip()}')
