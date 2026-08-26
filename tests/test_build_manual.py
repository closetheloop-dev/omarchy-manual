# SPDX-License-Identifier: Unlicense
"""Unit tests for scripts/build-manual.py.

Uses only the standard library (unittest) so it runs with `python3 -m unittest`
without any pip dependency. The builder script has a hyphen in its filename and
cannot be imported normally, so it is loaded via importlib.
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build-manual.py"


def _load_builder():
    spec = importlib.util.spec_from_file_location("build_manual", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bm = _load_builder()


def _build(chapters: dict[str, str]) -> str:
    """Write the given {filename: markdown} chapters to a temp dir and build them."""
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)
        for name, text in chapters.items():
            (path / name).write_text(text, encoding="utf-8")
        return bm.build(path)


class GithubSlugTests(unittest.TestCase):
    def test_spaces_become_hyphens(self):
        self.assertEqual(bm.github_slug("Hello World"), "hello-world")

    def test_punctuation_removed(self):
        self.assertEqual(bm.github_slug("What's new?"), "whats-new")

    def test_html_tags_stripped(self):
        self.assertEqual(bm.github_slug("Title <code>x</code>"), "title-x")


class HeadingFragmentTests(unittest.TestCase):
    def test_duplicate_headings_get_numbered_suffix(self):
        fragments = bm.heading_fragments("# Setup\n\n## Config\n\n## Config\n")
        self.assertIn("setup", fragments)
        self.assertIn("config", fragments)
        self.assertIn("config-1", fragments)


class BuildTests(unittest.TestCase):
    HAPPY = {
        "01-intro.md": "# Intro\n\nSee [nav](02-nav.md) and [tiling](02-nav.md#tiling).\n\n![diagram](images/x.webp)\n",
        "02-nav.md": "# Navigation\n\n## Tiling\n\nBody.\n",
    }

    def test_happy_path(self):
        out = _build(self.HAPPY)
        self.assertNotIn("![", out)  # image stripped
        self.assertNotIn("<a id=", out)
        self.assertIn("(#chapter-2-navigation)", out)
        self.assertIn("(#tiling)", out)
        self.assertIn("# Chapter 1: Intro", out)
        self.assertIn("# Chapter 2: Navigation", out)

    def test_link_to_missing_chapter_raises(self):
        with self.assertRaises(bm.BuildError):
            _build({"01-intro.md": "# Intro\n\n[x](99-missing.md)\n"})

    def test_link_to_missing_fragment_raises(self):
        with self.assertRaises(bm.BuildError):
            _build(
                {
                    "01-intro.md": "# Intro\n\n[x](02-nav.md#nope)\n",
                    "02-nav.md": "# Navigation\n",
                }
            )

    def test_duplicate_heading_link_uses_combined_document_suffix(self):
        out = _build(
            {
                "01-one.md": "# One\n\n## Shared\n",
                "02-two.md": "# Two\n\n## Shared\n",
                "03-three.md": "# Three\n\nSee [second shared](02-two.md#shared).\n",
            }
        )
        self.assertIn("[second shared](#shared-1)", out)

    def test_inline_image_raises(self):
        with self.assertRaises(bm.BuildError):
            _build({"01-intro.md": "# Intro\n\nText ![x](images/y.webp) more.\n"})

    def test_empty_source_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(bm.BuildError):
                bm.build(Path(directory))

    def test_unnumbered_chapter_raises(self):
        with self.assertRaises(bm.BuildError):
            _build({"intro.md": "# Intro\n"})

    def test_chapter_without_top_level_heading_raises(self):
        with self.assertRaises(bm.BuildError):
            _build({"01-intro.md": "## Intro\n"})


if __name__ == "__main__":
    unittest.main()
