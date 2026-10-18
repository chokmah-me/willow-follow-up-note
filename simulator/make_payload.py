import json, pathlib
here = pathlib.Path(__file__).parent
brief = (here / "ASTRA-BRIEF.md").read_text()
payload = {
    "model": "openai/gpt-6-astra",
    "messages": [
        {"role": "system", "content": "You are an expert Python developer writing research code. Follow the brief exactly. Output only the two files as fenced code blocks, each preceded by one line naming the file. No other prose."},
        {"role": "user", "content": brief},
    ],
    "max_tokens": 32000,
    "usage": {"include": True},
}
(here / "astra-payload.json").write_text(json.dumps(payload))
print("payload bytes", len(json.dumps(payload)))
