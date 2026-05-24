# Log Error Explainer

AI-powered log analyzer that turns cryptic stack traces into plain-English root cause + suggested fixes. Works with any OpenAI-compatible API including MiMo, DeepSeek, and OpenAI.

## Setup

```bash
export AI_API_URL="https://api.openai.com/v1"
export AI_API_KEY="***"
export AI_MODEL="gpt-4o-mini"  # or mimo-7b-rl, deepseek-chat, etc.
```

## Usage

```bash
# Analyze a log file
python3 explainer.py error.log

# Pipe from stdin
cat traceback.txt | python3 explainer.py -

# Specify source language
python3 explainer.py crash.log --language node

# Save to file
python3 explainer.py error.log --output analysis.md
```

## Output Format

The explainer produces four sections:

1. Root cause (one sentence)
2. Why it happened
3. Concrete fix with code example
4. Prevention notes

## Features

- Works with any OpenAI-compatible API (OpenAI, MiMo, DeepSeek, etc.)
- Stdin support for pipeline use
- Language hint for better diagnosis (python, node, go, rust, java)
- Output to stdout or file
