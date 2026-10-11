# DITA Topic Generator

A Python tool that turns raw, unstructured feature notes into well-formed DITA topics (task, concept, or reference) using the Claude API.

## Why

Developers and product teams often hand over information as quick notes. Turning those notes into structured DITA topics takes time. This tool creates a first draft in seconds, so the technical writer can focus on review and quality.

## Example

**Input** (`examples/charging-the-battery.txt`):

```
charging: take battery off bike first (key, turn left). plug charger into wall
socket, then connect to battery port - not the other way round!! ...
```

**Output** (`output/charging-the-battery.dita`): a DITA task with a gerund title, a prerequisite, one action per step, and the safety information as a caution note.

## How it works

1. The tool reads a plain text file with a raw description.
2. It sends the text to the Claude API together with DITA authoring rules for the selected topic type.
3. It checks that the returned XML is well-formed before saving it. Malformed output is never saved.

## Requirements

- Python 3.10 or later
- An Anthropic API key

## Installation

```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-api-key"
```

## Usage

```bash
python dita_generator.py examples/charging-the-battery.txt --type task
python dita_generator.py examples/battery-management-system.txt --type concept
python dita_generator.py examples/battery-specifications.txt --type reference
```

The generated topics are saved in the `output` folder.

## What I learned

- AI produces a strong first draft, but it still needs a technical writer. In testing, the model repeated the product name in every sentence, wrote a short description that talked about "this topic", and once described the battery as "lithium-free-claim-neutral".
- Well-formed XML is not the same as correct content. The script catches broken XML, but only a human catches a wrong sentence.
- Clear authoring rules in the prompt, such as "one action per step" and "do not invent facts", make the output much more reliable.

## Note

Kivra Battery is a fictional product created for demonstration purposes.

## Author

Mohamed Arshe, Technical Writer
[LinkedIn](https://www.linkedin.com/in/mohamed-arshe-083b712ba/) 
[GitHub](https://github.com/marshe-tw)
