# 🧩 Streaming YAML-to-JSON: A Reactive Partial Parser for LLM Outputs

This module allows you to stream YAML line-by-line or token-by-token (as if it's coming from an LLM), and **parse whatever is valid so far** into a structured JSON — even while the generation is still in progress.

It's ideal for:
- UI components that want to **render partial responses immediately in widgets**
- Avoiding the complexity of JSON parsing failures mid-stream
- Structured chat or agent interfaces

---

## 🚀 Features

- 🧠 **Smart YAML parsing:** Handles incomplete or broken YAML fragments.
- 🔁 **Quote-fix logic:** Appends missing `"` when needed to salvage partial strings.
- 🧱 **Template-aware merging:** Combines partial data with a fixed JSON skeleton.
- 🖼️ **UI-ready output:** Always returns a complete JSON structure with placeholders where data hasn't streamed yet.

---

## 📦 Install

No package install needed — just copy the code.

Make sure you already define the template JSON with empty values but all the keys that you want in UI.
The code uses streamed YAML to update that JSON so that in UI you get all keys — you just need to check for `null` values.

```
pip install pyyaml
```

---

## 🧪 Minimal Example (Simulated Stream)

```
from stream_yaml import YamlTokenStreamer, try_partial_yaml_parse, merge_yaml_into_template

template = {
  "user": {"id": None, "name": None, "roles": []},
  "lastLogin": None
}

yaml_text = """
user:
  id: 1
  name: "Medhavi"
  roles:
    - "developer"

lastLogin: "2025-06-02T10:00:00Z"
"""

t = ""
streamer = YamlTokenStreamer(yaml_text)
for token in streamer:
    t += token
    parsed, _ = try_partial_yaml_parse(t)
    merged = merge_yaml_into_template(template, parsed)
    print(merged)  # Always structured, even if partially filled
```

---

## ⚡ OpenAI Streaming Integration (with `openai.ChatCompletion.create`)

You can use this with OpenAI's streaming API like this:

```
import openai

buffer = ""
for chunk in openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Give me a YAML block for a user profile"}],
    stream=True,
):
    if 'content' in chunk['choices'][0].delta:
        token = chunk['choices'][0].delta['content']
        buffer += token

        parsed, _ = try_partial_yaml_parse(buffer)
        merged = merge_yaml_into_template(template, parsed)
        print(merged)  # Ready to render in UI
```

---

## 🔧 Customize It

You can:
- Replace `YamlTokenStreamer` with your own OpenAI stream wrapper.
- Change the `json_template` to match your app's needs.
- Turn the `merged` JSON into React state updates, Dash widgets, etc.

---

## 📄 License

MIT. Do whatever you want — just give credit if this saved you time. 🙂
