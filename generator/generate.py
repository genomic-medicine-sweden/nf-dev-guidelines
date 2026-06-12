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


class Config:
    def __init__(self, config_path: Path, guidelines_dir: Path, repo_root: Path):
        self._guidelines_dir = guidelines_dir
        self._repo_root = repo_root

        with open(config_path) as f:
            self._dict = yaml.safe_load(f)

        for field in ("title", "sections"):
            if field not in self._dict:
                sys.exit(f"ERROR: Missing required field '{field}' in {config_path}")

        self.title: str = self._dict["title"]
        self.sections: list = self._dict["sections"]
        self.variables: dict[str, Any] = {
            name: value.strip() if isinstance(value, str) else value
            for name, value in self._dict.get("vars", {}).items()
        }

    def _render_string(self, text: str, source_name: str) -> str:
        env = Environment(loader=BaseLoader(), **_JINJA_DEFAULTS)
        try:
            return env.from_string(text).render(**self.variables)
        except UndefinedError as e:
            sys.exit(f"ERROR: Undefined variable in {source_name}: {e}")

    def _render_section(self, item, sections_env: Environment) -> str:
        if isinstance(item, str):
            filename = f"{item}.md"
            try:
                template = sections_env.get_template(filename)
            except Exception:
                sys.exit(f"ERROR: Section '{item}' not found at {self._guidelines_dir / 'sections' / filename}")
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
        rendered_sections = [self._render_section(item, sections_env) for item in self.sections]

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
def main(config_path: Path, guidelines_dir: Path, repo_root: Path, output_path: Path) -> None:
    """Generate CONTRIBUTING.md from shared guidelines and repo config."""
    config = Config(
        config_path=config_path.resolve(),
        guidelines_dir=guidelines_dir.resolve(),
        repo_root=repo_root.resolve(),
    )
    output_path = output_path.resolve()
    output_path.write_text(config.to_string())
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
