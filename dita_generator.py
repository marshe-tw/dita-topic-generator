import argparse
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import anthropic

COMMON_RULES = """
- Start with the XML declaration and the correct DITA 1.3 DOCTYPE.
- Write in English, clear and concise, present tense.
- Write the product name consistently as "Kivra Battery".
- Do not invent facts that are not in the description.
- Return ONLY the XML. No explanations, no Markdown code fences.
"""

TYPE_RULES = {
    "task": """Create a DITA task topic.
- Use a gerund title (e.g. "Charging the battery").
- Write a one-sentence <shortdesc> stating the user's goal.
- Put conditions into <prereq>.
- Each <step> contains exactly one action in <cmd>; extra details go into <info>.
- Put warnings into <note type="caution"> inside the relevant step.
- Put the outcome into <result>.""",
    "concept": """Create a DITA concept topic.
- Use a noun-phrase title.
- Write a one-sentence <shortdesc>.
- Explain the concept in <conbody> with short paragraphs.
- Put reassurance or important context into <note>.""",
    "reference": """Create a DITA reference topic.
- Use a noun-phrase title.
- Write a one-sentence <shortdesc>.
- Present data in a <properties> table with <proptype> and <propvalue>.""",
}


def generate_topic(description: str, topic_type: str) -> str:
    client = anthropic.Anthropic()
    prompt = (
        "You are an expert DITA technical writer.\n\n"
        f"{TYPE_RULES[topic_type]}\n{COMMON_RULES}\n"
        f"Raw description:\n{description}"
    )
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    xml = "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()
    xml = xml.replace("```xml", "").replace("```", "").strip()
    end_tag = f"</{topic_type}>"
    start = xml.rfind("<?xml")
    end = xml.rfind(end_tag)
    if start != -1 and end != -1:
        xml = xml[start:end + len(end_tag)]
    return xml


def is_well_formed(xml: str) -> bool:
    try:
        ET.fromstring(xml.encode("utf-8"))
        return True
    except ET.ParseError as error:
        print(f"Invalid XML: {error}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate DITA topics from raw descriptions.")
    parser.add_argument("input", help="Path to the raw description (.txt)")
    parser.add_argument("--type", required=True, choices=TYPE_RULES.keys())
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Please set the ANTHROPIC_API_KEY environment variable.")

    input_path = Path(args.input)
    description = input_path.read_text(encoding="utf-8")

    print(f"Generating {args.type} topic from {input_path.name} ...")
    xml = generate_topic(description, args.type)

    if not is_well_formed(xml):
        print(xml)
        sys.exit("Topic was not saved.")

    output_path = Path("output") / f"{input_path.stem}.dita"
    output_path.write_text(xml, encoding="utf-8")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()