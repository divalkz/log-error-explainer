#!/usr/bin/env python3
"""
Log Error Explainer - Explain stack traces and error logs using AI.
Reads error logs and produces plain-English root cause + suggested fix.
"""

import os
import sys
import argparse
import requests


def get_api_config():
    """Load API config from environment variables."""
    api_url = os.environ.get("AI_API_URL")
    api_key = os.environ.get("AI_API_KEY")
    model = os.environ.get("AI_MODEL", "gpt-4o-mini")

    if not api_url or not api_key:
        sys.exit("Set AI_API_URL and AI_API_KEY environment variables.")

    return api_url, api_key, model


def read_log(filepath):
    """Read log file content."""
    if filepath == "-":
        return sys.stdin.read()
    if not os.path.exists(filepath):
        sys.exit(f"File not found: {filepath}")
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def explain(content, api_url, api_key, model, language="python"):
    """Send error log to AI API for root cause analysis."""
    system_prompt = (
        f"You are a senior {language} engineer. Given an error log or stack trace, "
        "produce: (1) Root cause in one sentence, (2) Why it happened, "
        "(3) Concrete fix with code example if applicable, (4) How to prevent it. "
        "Be concise and technical. Skip filler."
    )

    resp = requests.post(
        f"{api_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content[:10000]},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def main():
    parser = argparse.ArgumentParser(description="Explain error logs using AI")
    parser.add_argument("file", help="Log file to analyze (use - for stdin)")
    parser.add_argument(
        "--language",
        "-l",
        default="python",
        help="Source language hint (python, node, go, rust, java)",
    )
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    api_url, api_key, model = get_api_config()

    print(f"Analyzing: {args.file}", file=sys.stderr)
    content = read_log(args.file)

    if not content.strip():
        sys.exit("Empty log content.")

    explanation = explain(content, api_url, api_key, model, args.language)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(explanation)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(explanation)


if __name__ == "__main__":
    main()
