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
        return (
            bool(self.CALLOUT_PATTERN.search(block))
            and not self.parser.state.isstate("blockquote")
            and not util.nearing_recursion_limit()
        )

    def run(self, parent: etree.Element, blocks: list[str]) -> None:
        block = blocks.pop(0)
        m = self.CALLOUT_PATTERN.search(block)
        assert m

        before = block[: m.start()]
        if before.strip():
            self.parser.parseBlocks(parent, [before])

        kind = m[2]
        fold = m[3]
        title = m[4]
        content = m[5] or ""

        # Create the main callout container with folding class if needed
        classes = ["callout"]
        if fold in ["+", "-"]:
            classes.append("is-collapsible")

        # Create the main callout container
        admon = etree.SubElement(
            parent, "div", {"class": " ".join(classes), "data-callout": kind.lower()}
        )

        # Create title container
        attrib = {"class": "callout-title"}
        if fold in ["+", "-"]:
            attrib["dir"] = "auto"
        title_container = etree.SubElement(admon, "div", attrib)

        # Add icon container
        icon_container = etree.SubElement(
            title_container, "div", {"class": "callout-icon"}
        )
        # For now, using simple emoji icons - you might want to replace with proper SVG icons
        icon_map = {
            "note": "📝",
            "abstract": "📄",
            "document": "📄",
            "info": "ℹ️",
            "todo": "✅",
            "tip": "💡",
            "success": "✅",
            "question": "❓",
            "warning": "⚠️",
            "failure": "❌",
            "danger": "⛔",
            "bug": "🐛",
            "example": "📋",
            "quote": "💬",
        }
        icon_container.text = icon_map.get(kind.lower(), "📝")

        # Add title text
        title_inner = etree.SubElement(
            title_container, "div", {"class": "callout-title-inner"}
        )
        title_inner.text = title.strip() if title.strip() else kind.title()

        # Add fold icon if needed
        if fold in ["+", "-"]:
            fold_div = etree.SubElement(
                title_container, "div", {"class": "callout-fold"}
            )
            fold_div.text = "▶️"

        # Only add content div if there is content
        if content.strip():
            content_div = etree.SubElement(admon, "div", {"class": "callout-content"})

            # Add dir="auto" to all paragraph elements in the content
            for p in content_div.findall(".//p"):
                p.set("dir", "auto")

            # Split content into lines and reconstruct blocks for nested processing
            lines = content.split("\n")
            nested_blocks = []
            current_block = []

            for line in lines:
                cleaned = self.clean(line)
                if cleaned:
                    current_block.append(cleaned)
                elif current_block:
                    nested_blocks.append(current_block)
                    current_block = []

            if current_block:
                # Join with explicit line breaks instead of just newlines
                joined_content = "\n<br/>\n".join(current_block)
                nested_blocks.append(joined_content)

            self.parser.state.set("blockquote")
            self.parser.parseBlocks(content_div, nested_blocks)

            # Add dir="auto" to all paragraph elements after parsing
            for p in content_div.findall(".//p"):
                p.set("dir", "auto")

            # Parse the entire content as a single chunk
            self.parser.state.reset()

        # Handle any remaining content
        if m.end() < len(block):
            blocks.insert(0, block[m.end() :])


class ObsidianCalloutsExtension(Extension):
    @classmethod
    def extendMarkdown(cls, md: Markdown) -> None:
        parser = md.parser
        parser.blockprocessors.register(
            ObsidianCalloutsBlockProcessor(md.parser),
            "obsidian-callouts",
            21.1,  # Priority just before blockquote
        )


makeExtension = ObsidianCalloutsExtension  # noqa: N816
