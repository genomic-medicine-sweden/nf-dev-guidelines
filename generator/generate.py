#!/usr/bin/env python3
"""Generate CONTRIBUTING.md from shared sections and repo-specific config."""

import re
import sys
from pathlib import Path
from typing import Any

import click
import yaml
from jinja2 import BaseLoader, Environment, FileSystemLoader, StrictUndefined, UndefinedError

REQUIRED_CONFIG_FIELDS = ("title", "intro", "sections")


def load_config(config_path: Path) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def validate_config(config: dict, config_path: Path) -> None:
    for field in REQUIRED_CONFIG_FIELDS:
        if field not in config:
            sys.exit(f"ERROR: Missing required field '{field}' in {config_path}")


def render_string(text: str, template_vars: dict, source_name: str) -> str:
    env = Environment(
        loader=BaseLoader(),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    try:
        return env.from_string(text).render(**template_vars)
    except UndefinedError as e:
        sys.exit(f"ERROR: Undefined variable in {source_name}: {e}")


def render_sections(
    section_items: list,
    sections_dir: Path,
    repo_root: Path,
    template_vars: dict,
) -> list[str]:
    env = Environment(
        loader=FileSystemLoader(str(sections_dir)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    rendered = []
    for item in section_items:
        if isinstance(item, str):
            filename = f"{item}.md"
            try:
                template = env.get_template(filename)
            except Exception:
                sys.exit(f"ERROR: Section '{item}' not found at {sections_dir / filename}")
            try:
                rendered.append(template.render(**template_vars).strip())
            except UndefinedError as e:
                sys.exit(f"ERROR: Undefined variable in section '{item}': {e}")
        elif isinstance(item, dict):
            file_rel = item.get("file")
            if not file_rel:
                sys.exit(f"ERROR: Custom section entry missing 'file': {item}")
            file_path = repo_root / file_rel
            if not file_path.exists():
                sys.exit(f"ERROR: Custom section file not found: {file_path}")
            raw = file_path.read_text().rstrip()
            rendered.append(render_string(raw, template_vars, source_name=f"custom section ({file_rel})").strip())
        else:
            sys.exit(f"ERROR: Invalid section entry: {item!r}")
    return rendered


def render_output(
    guidelines_dir: Path,
    config: dict,
    intro: str,
    rendered_sections: list[str],
) -> str:
    env = Environment(
        loader=FileSystemLoader(str(guidelines_dir / "templates")),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("CONTRIBUTING.md.j2")
    return template.render(
        title=config["title"],
        intro=intro,
        rendered_sections=rendered_sections,
    )


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
    config_path = config_path.resolve()
    guidelines_dir = guidelines_dir.resolve()
    repo_root = repo_root.resolve()
    output_path = output_path.resolve()

    config = load_config(config_path)
    validate_config(config, config_path)
    raw_vars: dict[str, Any] = config.get("vars", {})
    template_vars: dict[str, Any] = {name: value.strip() if isinstance(value, str) else value for name, value in raw_vars.items()}

    intro = render_string(
        text=config["intro"].strip(),
        template_vars=template_vars,
        source_name="intro field in config",
    )

    rendered_sections = render_sections(
        section_items=config["sections"],
        sections_dir=guidelines_dir / "sections",
        repo_root=repo_root,
        template_vars=template_vars,
    )

    output = render_output(
        guidelines_dir=guidelines_dir,
        config=config,
        intro=intro,
        rendered_sections=rendered_sections,
    )
    output = re.sub(r"\n{3,}", "\n\n", output).rstrip("\n") + "\n"
    output_path.write_text(output)
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
