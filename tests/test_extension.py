import re

import bs4
import pytest
from markdown import Markdown

from markdown_callouts.callouts import CalloutsExtension
from markdown_callouts.github_callouts import GitHubCalloutsExtension
from markdown_callouts.obsidian_callouts import ObsidianCalloutsExtension

extension_styles = {
    "callouts": CalloutsExtension,
    "github": GitHubCalloutsExtension,
    "obsidian": ObsidianCalloutsExtension,
}


@pytest.mark.golden_test("callouts/**/*.yml", "github/**/*.yml", "obsidian/**/*.yml", "all/**/*.yml")
def test_extension(request, golden):
    config = {k: golden[k] for k in ["strip_period"] if golden.get(k) is not None}
    extensions = [
        extension(**config)
        for key, extension in extension_styles.items()
        if f"{key}/" in request.node.name or "all/" in request.node.name
    ]
    md = Markdown(extensions=extensions)
    output = md.convert(golden["input"])
    actual_soup = bs4.BeautifulSoup(output, features="html.parser")
    expected_soup = bs4.BeautifulSoup(golden.out["output"], features="html.parser")

    assert actual_soup.prettify() == expected_soup.prettify()
