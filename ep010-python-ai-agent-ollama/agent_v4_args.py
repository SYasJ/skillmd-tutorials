"""A tiny AI agent in plain Python: Ollama + 3 tools + a loop. No framework."""
import ast, datetime, inspect, operator, pathlib, sys
from ollama import chat

MODEL = "qwen3:1.7b"
NOTES = pathlib.Path("notes").resolve()

def get_today() -> str:
    """Get today's date (YYYY-MM-DD)."""
    return datetime.date.today().isoformat()

def calculate(expression: str) -> str:
    """Do arithmetic, e.g. '(30 - 2) * 24'. Numbers and + - * / only."""
    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in ops: return ops[type(n.op)](ev(n.left), ev(n.right))
        raise ValueError("only numbers and + - * /")
    return str(ev(ast.parse(expression, mode="eval").body))

def read_file(name: str) -> str:
    """Read a text file from the notes folder."""
    path = (NOTES / name).resolve()
    if NOTES not in path.parents: return "ERROR: only files inside notes/ are allowed"
    return path.read_text()

SYSTEM = ("You are an agent working in a loop. Call tools whenever they help, "
          "as many times as you need. Use tool results, never guess dates or math. "
          "When you are done, reply with the final answer only.")

TOOLS = {f.__name__: f for f in (get_today, calculate, read_file)}

def run(question: str, max_steps: int = 6) -> str:
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        reply = chat(model=MODEL, messages=messages, tools=list(TOOLS.values()), think=False)
        messages.append(reply.message)
        if not reply.message.tool_calls:
            return reply.message.content          # no tool asked for -> final answer
        for call in reply.message.tool_calls:
            name, args = call.function.name, call.function.arguments
            if name in TOOLS:                      # drop arguments the tool doesn't have
                args = {k: v for k, v in args.items() if k in inspect.signature(TOOLS[name]).parameters}
            try:
                result = TOOLS[name](**args)
            except Exception as e:                 # give the error BACK to the model
                result = f"ERROR: {e}"
            print(f"  step {step}: {name}({args}) -> {result!r}")
            messages.append({"role": "tool", "tool_name": name, "content": result})
    return "Stopped: too many steps."

if __name__ == "__main__":
    print("ANSWER:", run(" ".join(sys.argv[1:])))
