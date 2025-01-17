from pathlib import Path
import markdown
from markdown_obsidian_callouts.obsidian_callouts import ObsidianCalloutsExtension
from jinja2 import Template


def convert_markdown_to_html(input_file: Path) -> None:
    """Convert a Markdown file to HTML with callouts support."""
    # Load template, styles and scripts
    template_path = Path("assets/template.html")
    styles_path = Path("assets/styles.css")
    scripts_path = Path("assets/callouts.js")

    html_template = template_path.read_text(encoding="utf-8")
    css_styles = styles_path.read_text(encoding="utf-8")
    js_scripts = scripts_path.read_text(encoding="utf-8")

    # Create markdown converter with extensions
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            ObsidianCalloutsExtension(),
        ]
    )

    # Read markdown content
    markdown_content = input_file.read_text(encoding="utf-8")

    # Convert to HTML
    html_content = md.convert(markdown_content)

    # Create HTML with template
    template = Template(html_template)
    final_html = template.render(
        title=input_file.stem, content=html_content, styles=css_styles, scripts=js_scripts
    )

    # Write output file
    output_file = input_file.with_suffix(".html")
    output_file.write_text(final_html, encoding="utf-8")
    print(f"Created {output_file}")


def main():
    # Convert all markdown files in examples directory
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)

    for md_file in examples_dir.glob("*.md"):
        convert_markdown_to_html(md_file)


if __name__ == "__main__":
    main()
