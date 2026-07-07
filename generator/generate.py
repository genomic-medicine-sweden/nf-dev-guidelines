#!/usr/bin/env python3
"""Generate CONTRIBUTING.md from shared sections and repo-specific config."""

import re
import sys
from pathlib import Path
from typing import Any

import click
import yaml
from jinja2 import BaseLoader, Environment, FileSystemLoader, StrictUndefined, UndefinedError

_JINJA_DEFAULTS: dict[str, Any] = dict(
    undefined=StrictUndefined,
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
)

# Canonical order used when a consuming repo's config omits 'sections:'. Keep in sync
# with sections/*.md — appending a name here is what makes a new shared section reach
# every consuming repo on its next sync without them touching their config.
DEFAULT_SECTIONS: list[str] = ["general", "coding_conventions", "updating_contribution_guidelines"]


class Config:
    def __init__(self, config_path: Path, guidelines_dir: Path, repo_root: Path):
        self._guidelines_dir = guidelines_dir
        self._repo_root = repo_root

        with open(config_path) as f:
            self._dict = yaml.safe_load(f)

        if "title" not in self._dict:
            sys.exit(f"ERROR: Missing required field 'title' in {config_path}")

        self.title: str = self._dict["title"]
        self.sections: list = self._resolve_sections(config_path)
        self.variables: dict[str, Any] = {
            name: value.strip() if isinstance(value, str) else value
            for name, value in self._dict.get("vars", {}).items()
        }

    def _resolve_sections(self, config_path: Path) -> list:
        if "sections" in self._dict:
            sys.exit(
                f"ERROR: {config_path} sets 'sections', which is no longer supported. Every consuming "
                "repo now gets all of DEFAULT_SECTIONS by default. Use 'exclude_sections:' to drop "
                "specific ones and 'custom_sections:' (with 'after:'/'before:' anchors) to interleave "
                "pipeline-specific content. See the nf-dev-guidelines README."
            )

        exclude = self._dict.get("exclude_sections")
        custom = self._dict.get("custom_sections")

        excluded = set(exclude or [])
        unknown_excludes = excluded - set(DEFAULT_SECTIONS)
        if unknown_excludes:
            print(
                f"WARNING: exclude_sections in {config_path} references unknown section(s): "
                f"{sorted(unknown_excludes)}",
                file=sys.stderr,
            )

        base = [name for name in DEFAULT_SECTIONS if name not in excluded]
        return self._insert_custom_sections(base, custom or [])

    @staticmethod
    def _insert_custom_sections(base: list[str], custom: list[dict]) -> list:
        """Interleave custom_sections into base, anchored via 'after'/'before' a default section name."""
        insertions: list[tuple[int, dict]] = []
        for entry in custom:
            file_rel = entry.get("file")
            if not file_rel:
                sys.exit(f"ERROR: custom_sections entry missing 'file': {entry}")
            after, before = entry.get("after"), entry.get("before")
            if after is not None and before is not None:
                sys.exit(f"ERROR: custom_sections entry for '{file_rel}' sets both 'after' and 'before'")
            if after is not None:
                if after not in base:
                    print(
                        f"WARNING: custom_sections entry for '{file_rel}' references 'after: {after}', which "
                        "isn't a current default section (removed or excluded?) — skipping this custom section. "
                        f"Update its anchor in your config. (available: {base})",
                        file=sys.stderr,
                    )
                    continue
                index = base.index(after) + 1
            elif before is not None:
                if before not in base:
                    print(
                        f"WARNING: custom_sections entry for '{file_rel}' references 'before: {before}', which "
                        "isn't a current default section (removed or excluded?) — skipping this custom section. "
                        f"Update its anchor in your config. (available: {base})",
                        file=sys.stderr,
                    )
                    continue
                index = base.index(before)
            else:
                index = len(base)
            insertions.append((index, {"file": file_rel}))

        result: list = list(base)
        offset = 0
        for index, item in sorted(insertions, key=lambda pair: pair[0]):
            result.insert(index + offset, item)
            offset += 1
        return result

    def _render_string(self, text: str, source_name: str) -> str:
        env = Environment(loader=BaseLoader(), **_JINJA_DEFAULTS)
        try:
            return env.from_string(text).render(**self.variables)
        except UndefinedError as e:
            sys.exit(f"ERROR: Undefined variable in {source_name}: {e}")

    def _render_section(self, item, sections_env: Environment) -> str | None:
        if isinstance(item, str):
            filename = f"{item}.md"
            try:
                template = sections_env.get_template(filename)
            except Exception:
                print(
                    f"WARNING: Section '{item}' not found at {self._guidelines_dir / 'sections' / filename} "
                    f"(removed upstream?) — skipping. Remove '{item}' from 'sections:' in your config.",
                    file=sys.stderr,
                )
                return None
            try:
                return template.render(**self.variables).strip()
            except UndefinedError as e:
                sys.exit(f"ERROR: Undefined variable in section '{item}': {e}")
        elif isinstance(item, dict):
            file_rel = item.get("file")
            if not file_rel:
                sys.exit(f"ERROR: Custom section entry missing 'file': {item}")
            file_path = self._repo_root / file_rel
            if not file_path.exists():
                sys.exit(f"ERROR: Custom section file not found: {file_path}")
            raw = file_path.read_text().rstrip()
            return self._render_string(text=raw, source_name=f"custom section ({file_rel})").strip()
        else:
            sys.exit(f"ERROR: Invalid section entry: {item!r}")

    def to_string(self) -> str:
        intro_raw = self._dict.get("intro", "")
        intro = self._render_string(text=intro_raw.strip(), source_name="intro field in config") if intro_raw else ""

        sections_env = Environment(
            loader=FileSystemLoader(str(self._guidelines_dir / "sections")),
            **_JINJA_DEFAULTS,
        )
        rendered_sections = [
            rendered
            for item in self.sections
            if (rendered := self._render_section(item, sections_env)) is not None
        ]

        output_env = Environment(
            loader=FileSystemLoader(str(self._guidelines_dir / "templates")),
            **_JINJA_DEFAULTS,
        )
        output = output_env.get_template("CONTRIBUTING.md.j2").render(
            title=self.title,
            intro=intro,
            rendered_sections=rendered_sections,
        )
        return re.sub(r"\n{3,}", "\n\n", output).rstrip("\n") + "\n"


@click.command()
@click.option(
    "--config",
    "config_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to the nf-dev-guidelines config file (e.g. assets/nf-dev-guidelines.yaml)",
)
@click.option(
    "--guidelines",
    "guidelines_dir",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Path to the nf-dev-guidelines repository root",
)
@click.option(
    "--repo-root",
    default=".",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Root of the consuming repository; custom section file paths are relative to this (default: CWD)",
)
@click.option(
    "--output",
    "output_path",
    default="docs/CONTRIBUTING.md",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Output file path (default: docs/CONTRIBUTING.md)",
)
def main(config_path: click.Path, guidelines_dir: click.Path, repo_root: click.Path, output_path: click.Path) -> None:
    """Generate CONTRIBUTING.md from shared guidelines and repo config."""
    config = Config(
        config_path=Path(config_path),
        guidelines_dir=Path(guidelines_dir),
        repo_root=Path(repo_root),
    )
    output_path = Path(output_path)
    output_path.write_text(config.to_string())
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
