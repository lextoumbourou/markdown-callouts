from pathlib import Path
import subprocess
import sys


def minify_css(input_path: Path, output_path: Path) -> None:
    """Minify CSS using postcss/cssnano."""
    try:
        subprocess.run(
            ["npx", "postcss", str(input_path), "--output", str(output_path), "--use", "cssnano"],
            check=True,
        )
    except subprocess.CalledProcessError:
        print("Error: Failed to minify CSS. Is npx/postcss installed?")
        sys.exit(1)


def minify_js(input_path: Path, output_path: Path) -> None:
    """Minify JavaScript using terser."""
    try:
        subprocess.run(
            [
                "npx",
                "terser",
                str(input_path),
                "--compress",
                "--mangle",
                "--output",
                str(output_path),
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        print("Error: Failed to minify JavaScript. Is npx/terser installed?")
        sys.exit(1)


def main():
    # Setup paths
    root = Path(__file__).parent.parent
    static_dir = root / "markdown_obsidian_callouts" / "static"
    static_dir.mkdir(exist_ok=True)

    # Minify CSS
    css_input = root / "assets" / "styles.css"
    css_output = static_dir / "callouts.min.css"
    minify_css(css_input, css_output)

    # Minify JS
    js_input = root / "assets" / "callouts.js"
    js_output = static_dir / "callouts.min.js"
    minify_js(js_input, js_output)


if __name__ == "__main__":
    main()
