import random
import yaml
import time
import json

json_template = {
  "user": {
    "id": None,
    "name": None,
    "active": None,
    "roles": [],
    "profile": {
      "age": None,
      "location": None,
      "skills": {
        "python": None,
        "c++": None,
        "cuda": None
      }
    }
  },
  "projects": [
    {
      "name": None,
      "openSource": None,
      "stars": None
    }
  ],
  "lastLogin": None
}

yaml_sample = """
user:
  id: 42
  name: "Medhavi"
  active: true
  roles:
    - "admin"
    - "developer"
    - "researcher"
  profile:
    age: 27
    location: "India"
    skills:
      python: "advanced"
      c++: "intermediate"
      cuda: "beginner"

projects:
  - name: "GreedyContext"
    openSource: true
    stars: 120
  - name: "Cortana++"
    openSource: true
    stars: 98

lastLogin: "2025-06-01T12:30:00Z"
"""

class YamlTokenStreamer:
    def __init__(self, yaml_text: str):
        self.yaml_text:str = yaml_text
        self.index = 0
        self.length = len(yaml_text)

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self.index >= self.length:
            raise StopIteration
        
        # Random chunk size between 1 and 10
        chunk_size = random.randint(1, 5)
        chunk = self.yaml_text[0 : self.index + chunk_size]
        time.sleep(0.5)
        self.index += chunk_size
        return chunk

def try_partial_yaml_parse(text: str):
    """
    Attempt to parse YAML text.
    If full parsing fails, backtrack line-by-line.
    Also try fixing broken quoted lines by appending `"`.
    Returns: (parsed_dict or None, lines_parsed or 0, used_quote_fix: bool)
    """
    def is_valid_yaml(yaml_text):
        try:
            parsed = yaml.safe_load(yaml_text)
            return parsed if isinstance(parsed, dict) else None
        except Exception:
            return None

    # Try full parse
    full = is_valid_yaml(text)
    if full:
        return full, len(text.splitlines())

    # Try partial lines
    lines = text.splitlines()
    for i in range(len(lines), 0, -1):
        chunk = "\n".join(lines[:i])
        parsed = is_valid_yaml(chunk)
        if parsed:
            return parsed, i

        # Try appending quote to last line
        fixed_lines = lines[:i]
        fixed_lines[-1] += '"'
        parsed_with_quote = is_valid_yaml("\n".join(fixed_lines))
        if parsed_with_quote:
            return parsed_with_quote, i

    return None, 0

def merge_yaml_into_template(template, parsed):
    if not isinstance(template, dict):
        return parsed if parsed is not None else None

    result = {}
    for key, val in template.items():
        if parsed is None:
            result[key] = val
        elif key not in parsed:
            result[key] = val
        elif isinstance(val, dict):
            result[key] = merge_yaml_into_template(val, parsed.get(key, {}))
        elif isinstance(val, list):
            parsed_list = parsed.get(key, [])
            result[key] = []
            for i, item in enumerate(val):
                if parsed_list is None:
                    break
                elif i < len(parsed_list):
                    result[key].append(merge_yaml_into_template(item, parsed_list[i]))
                else:
                    result[key].append(item)
            else:
                result[key] = parsed.get(key, [])
        elif isinstance(parsed, dict):
            result[key] = parsed.get(key, val)
    return result


streamer = YamlTokenStreamer(yaml_sample)
for token in streamer:
    print("🔹 Streamed so far:\n", token)

    parsed, lines_used = try_partial_yaml_parse(token)
    print(parsed)
    if parsed:
        merged = merge_yaml_into_template(json_template, parsed)
        print("✅ Fully aligned JSON:")
        print(json.dumps(merged, indent=2))
    else:
        print("❌ Not yet valid YAML.\n")
