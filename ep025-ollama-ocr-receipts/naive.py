"""What happens when you just ask for JSON, with no schema."""
import sys

from ollama import chat


def main() -> None:
    reply = chat(
        model="glm-ocr:q8_0",
        messages=[{
            "role": "user",
            "content": "Extract this receipt as JSON.",
            "images": [sys.argv[1]],
        }],
        options={"temperature": 0},
    )
    print(reply.message.content)


if __name__ == "__main__":
    main()
