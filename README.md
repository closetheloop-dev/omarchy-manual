# Omarchy Quattro Manual

An unofficial, agent-friendly, single-file mirror of the [official Omarchy Quattro manual](https://github.com/basecamp/omarchy/tree/quattro/manual).

The generated manual is available at [`omarchy-quattro-manual.md`](https://raw.githubusercontent.com/closetheloop-dev/omarchy-manual/main/omarchy-quattro-manual.md). Point an agent at this raw URL when it needs the complete Omarchy Quattro user documentation in one context:

```text
https://raw.githubusercontent.com/closetheloop-dev/omarchy-manual/main/omarchy-quattro-manual.md
```

## What this repository does

Every six hours, the GitHub Actions workflow:

1. Fetches the `quattro` branch of [`basecamp/omarchy`](https://github.com/basecamp/omarchy).
2. Concatenates the numbered manual chapters in order.
3. Prefixes each top-level heading with its chapter number.
4. Rewrites links between chapters as links within the combined document.
5. Removes image references to keep the result text-only and self-contained.
6. Updates `omarchy-quattro-manual.md` when the generated content changes.

The generated file should not be edited directly.

## Build locally

With the Omarchy repository cloned alongside this repository as `omarchy`:

```bash
python3 scripts/build-manual.py \
  --source ../omarchy/manual \
  --output omarchy-quattro-manual.md
```

The builder uses only the Python standard library. It fails when a chapter link cannot be resolved or when the source contains an image format it cannot safely remove.

Run the builder tests with:

```bash
python3 -B -m unittest discover -s tests -v
```

## Attribution and licensing

The manual is sourced from [Omarchy](https://github.com/basecamp/omarchy), created by David Heinemeier Hansson. The generated manual remains covered by Omarchy's [`LICENSE`](LICENSE).

The build, test, and automation files created for this repository are released into the public domain under the [`UNLICENSE`](UNLICENSE).

This repository is not an official Omarchy or Basecamp project.
