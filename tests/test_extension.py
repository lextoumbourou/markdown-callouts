import yaml
from pathlib import Path
import bs4
import pytest
from markdown import Markdown

from markdown_obsidian_callouts.obsidian_callouts import ObsidianCalloutsExtension


@pytest.fixture
def extension_styles():
    return {
        "obsidian": ObsidianCalloutsExtension,
    }


def load_test_cases():
    fixtures_dir = Path(__file__).parent / "fixtures" / "test_cases"
    test_cases = []

    for yml_file in fixtures_dir.rglob("*.yml"):
        test_cases.append(pytest.param(yml_file, id=str(yml_file.relative_to(fixtures_dir))))
    return test_cases


@pytest.mark.parametrize("fixture_path", load_test_cases())
def test_extension(fixture_path: Path, extension_styles):
    # Load YAML content
    with open(fixture_path) as f:
        golden = yaml.safe_load(f)

    # Extract config from fixture
    config = {k: golden[k] for k in ["strip_period"] if golden.get(k) is not None}

    # Setup extensions based on fixture path
    extensions = [
        extension(**config)
        for key, extension in extension_styles.items()
        if f"{key}/" in str(fixture_path) or "all/" in str(fixture_path)
    ]

    md = Markdown(extensions=extensions)
    output = md.convert(golden["input"])

    actual_soup = bs4.BeautifulSoup(output, features="html.parser")
    expected_soup = bs4.BeautifulSoup(golden["output"], features="html.parser")

    assert actual_soup.prettify() == expected_soup.prettify()
