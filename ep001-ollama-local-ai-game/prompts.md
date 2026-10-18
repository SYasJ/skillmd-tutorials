# The exact commands from the video

All three were run on a Mac with Ollama 0.30.11 and `qwen2.5-coder:3b` (1.9 GB). Times are what we measured on that run.

## 1 · Get the model (75 s)
```bash
ollama --version
ollama pull qwen2.5-coder:3b
```

## 2 · Try 1: one vague line (135 s) — what went wrong #1
```bash
ollama run qwen2.5-coder:3b "Make a Snake game in one HTML file with CSS and JavaScript. Arrow keys to move, show the score, restart on game over. Only output the code." | tee snake.html
```
The model wrapped the code in chat text and ``` fences, so `snake.html` was not a working page.

## 3 · Try 2: be specific (110 s) — what went wrong #2
```bash
ollama run qwen2.5-coder:3b --nowordwrap "Make a Snake game in one HTML file. Use a 400x400 canvas with a 20x20 grid. Draw the score on the canvas. Arrow keys to move. Press space to restart after game over. Output only the code, no explanation." | tee raw2.txt
sed -n '/<!DOCTYPE/,/<\/html>/p' raw2.txt > snake.html
```
Result: `snake-try2-buggy.html`. It runs, but the snake starts at x 150 while food sits on multiples of 20 (it can never eat), and it can leave the canvas.

## 4 · Make it fix its own bugs (150 s)
```bash
cat snake.html | ollama run qwen2.5-coder:3b --nowordwrap "Fix this Snake game. Bug 1: the snake starts at x 150, so it never lines up with the food on the 20px grid. Start it at 200,200. Bug 2: the snake can leave the canvas. End the game when it hits a wall. Output only the full fixed HTML file." | tee raw3.txt
sed -n '/<!DOCTYPE/,/<\/html>/p' raw3.txt > snake-fixed.html
```
Result: `snake-fixed.html` — open it in any browser and use the arrow keys.

## My 3 rules
1. Test what it gives you.
2. Read the code (or at least skim it).
3. Give it the exact bug, not "it doesn't work".
