from __future__ import annotations

import re
import xml.etree.ElementTree as etree

from markdown import Markdown, util
from markdown.blockprocessors import BlockQuoteProcessor
from markdown.extensions import Extension


class ObsidianCalloutsBlockProcessor(BlockQuoteProcessor):
    CALLOUT_PATTERN = re.compile(
        r"""
        # Group 1: Leading content/whitespace
        ((?:^|\n) *(?:[^>].*)?(?:^|\n))

        # Callout start: up to 3 spaces followed by >
        [ ]{0,3}>[ ]*

        # Group 2: Callout type inside [! ]
        \[!([A-Za-z0-9_-]+)\]

        # Group 3: Optional fold marker (+ or -)
        ([-+]?)[ ]*

        # Group 4: Title text
        (.*?)(?:\n|$)

        # Group 5: Content (lines starting with >)
        ((?:(?:>[ ]*[^\n]*\n?)*))
        """,
        flags=re.MULTILINE | re.IGNORECASE | re.VERBOSE,
    )

    def test(self, parent, block):
        # Allow callouts even inside blockquotes, so we can nest them
        return (
            bool(self.CALLOUT_PATTERN.search(block))
            and not util.nearing_recursion_limit()
        )

    def run(self, parent: etree.Element, blocks: list[str]) -> None:
        """
        1. Match: > [!type] Title
        2. Extract all lines that start with '>'
        3. Inside those lines, detect further nested callouts or treat them as multi-line text
        """
        block = blocks.pop(0)
        m = self.CALLOUT_PATTERN.search(block)
        if not m:
            return

        # Anything before this callout gets parsed normally
        before = block[: m.start()]
        if before.strip():
            self.parser.parseBlocks(parent, [before])

        kind = m.group(2)
        fold = m.group(3)
        title = m.group(4)
        content = m.group(5) or ""

        # Build outer <div>
        div_classes = ["callout"]
        if fold in ["+", "-"]:
            div_classes.append("is-collapsible")

        callout_div = etree.SubElement(
            parent,
            "div",
            {"class": " ".join(div_classes), "data-callout": kind.lower()},
        )

        # Title container
        title_attrs = {"class": "callout-title"}
        if fold in ["+", "-"]:
            title_attrs["dir"] = "auto"
        title_container = etree.SubElement(callout_div, "div", title_attrs)

        # Icon mapping using Lucide icon names
        icon_map = {
            "note": "pencil",
            "abstract": "clipboard",
            "document": "file-text",
            "info": "info",
            "todo": "check-circle",
            "tip": "lightbulb",
            "success": "check",
            "question": "help-circle",
            "warning": "alert-triangle",
            "failure": "x-circle",
            "danger": "alert-octagon",
            "bug": "bug",
            "example": "list",
            "quote": "quote",
        }
        
        icon_el = etree.SubElement(
            title_container, 
            "div", 
            {
                "class": "callout-icon",
                "data-lucide": icon_map.get(kind.lower(), "pencil")
            }
        )
        assert not icon_el.text

        # Title text
        title_inner = etree.SubElement(
            title_container,
            "div",
            {"class": "callout-title-inner"},
        )
        title_inner.text = title.strip() if title.strip() else kind.title()

        # Fold icon if needed
        if fold in ["+", "-"]:
            fold_el = etree.SubElement(
                title_container, 
                "div", 
                {
                    "class": "callout-fold",
                    "data-lucide": "chevron-down"
                }
            )

        # Parse the callout body
        if content.strip():
            content_div = etree.SubElement(
                callout_div, "div", {"class": "callout-content"}
            )
            lines = content.split("\n")

            # Group lines into regular text and nested callouts
            text_lines = []
            idx = 0

            while idx < len(lines):
                line = lines[idx].lstrip(">").lstrip()

                # Check if this line starts a nested callout
                if "[!" in line and "]" in line:  # Quick pre-check for performance
                    # If we have accumulated text, process it first
                    if text_lines:
                        p = etree.SubElement(content_div, "p", {"dir": "auto"})
                        # Join with explicit <br/> tags
                        p.text = "\n   ".join(
                            line if i == len(text_lines) - 1 else line + "<br/>"
                            for i, line in enumerate(text_lines)
                        )
                        text_lines = []

                    # Collect the nested callout and all its content
                    nested_block = []
                    while idx < len(lines):
                        line = lines[idx]
                        # Remove one level of '>' prefix for proper nesting
                        if line.startswith("> "):
                            line = line[2:]
                        nested_block.append(line)
                        idx += 1
                        if idx < len(lines) and not lines[idx].startswith(">"):
                            break

                    # Process the nested callout
                    self.parser.parseChunk(content_div, "\n".join(nested_block))
                else:
                    if line.strip():
                        text_lines.append(line)
                    idx += 1

            # Process any remaining text
            if text_lines:
                p = etree.SubElement(content_div, "p", {"dir": "auto"})
                # Join lines with <br/> for proper line breaks
                p.text = "\n   ".join(
                    line if i == len(text_lines) - 1 else line + "<br/>"
                    for i, line in enumerate(text_lines)
                )

        # If there's leftover text after the match, reinsert it
        if m.end() < len(block):
            blocks.insert(0, block[m.end() :])


class ObsidianCalloutsExtension(Extension):
    @classmethod
    def extendMarkdown(cls, md: Markdown) -> None:
        # Register at a priority just before the standard blockquote
        md.parser.blockprocessors.register(
            ObsidianCalloutsBlockProcessor(md.parser),
            "obsidian-callouts",
            21.1,
        )


makeExtension = ObsidianCalloutsExtension  # noqa: N816
