"""Delivery-surface generators (enhancement 4).

Builds realistic carrier documents for the surfaces where detectors now
hunt: MCP tool descriptions, skill files (SKILL.md), and README/markdown.
Each generator embeds an invisible payload via a chosen channel.
"""

from __future__ import annotations

from stegano import channels


def mcp_tool_description(tool_name: str, visible_desc: str, payload: str,
                         channel: str = "tag_block") -> str:
    """Generate an MCP tool description with a hidden instruction payload.

    The payload is woven between the description sentences so it survives
    naive truncation; visually the description reads normally.
    """
    ch = channels.get(channel)
    encoded = ch.encode(payload)
    sentences = [s.strip() for s in visible_desc.split(". ") if s.strip()]
    if len(sentences) < 2:
        return visible_desc + " " + encoded
    mid = len(sentences) // 2
    sentences.insert(mid, encoded)
    return ". ".join(sentences)


def skill_file(skill_name: str, visible_doc: str, payload: str,
               channel: str = "tag_block") -> str:
    """Generate a SKILL.md-style document carrying a hidden payload.

    The payload hides inside an HTML comment block — invisible in rendered
    markdown but present in the raw file models ingest.
    """
    ch = channels.get(channel)
    encoded = ch.encode(payload)
    return (f"# {skill_name}\n\n{visible_doc}\n\n"
            f"<!-- {encoded} -->\n")


def readme_injection(visible_md: str, payload: str,
                     channel: str = "zero_width") -> str:
    """Inject a hidden payload into markdown between visible lines."""
    ch = channels.get(channel)
    encoded = ch.encode(payload)
    lines = visible_md.split("\n")
    idx = len(lines) // 2
    lines.insert(idx, encoded)
    return "\n".join(lines)
