#!/usr/bin/env python3
"""Generate CONTRIBUTING.md from shared sections and repo-specific config."""

import argparse
import re
import sys
from pathlib import Path

import yaml
from jinja2 import BaseLoader, Environment, FileSystemLoader, StrictUndefined, UndefinedError

REQUIRED_CONFIG_FIELDS = ("title", "intro", "sections")


def load_config(config_path: Path) -> dict:
    with open(config_path) as f:
        config = yaml.safe_load(f)
    for field in REQUIRED_CONFIG_FIELDS:
        if field not in config:
            sys.exit(f"ERROR: Missing required field '{field}' in {config_path}")
    return config


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
    section_names: list[str],
    sections_dir: Path,
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
    for name in section_names:
        filename = f"{name}.md"
        try:
            template = env.get_template(filename)
        except Exception:
            sys.exit(f"ERROR: Section '{name}' not found at {sections_dir / filename}")
        try:
            rendered.append(template.render(**template_vars).strip())
        except UndefinedError as e:
            sys.exit(f"ERROR: Undefined variable in section '{name}': {e}")
    return rendered


def load_custom_sections(
    custom_section_defs: list[dict],
    repo_root: Path,
    template_vars: dict,
) -> list[dict]:
    sections = []
    for item in custom_section_defs:
        title = item.get("title")
        file_rel = item.get("file")
        if not title:
            sys.exit(f"ERROR: Custom section missing 'title': {item}")
        if not file_rel:
            sys.exit(f"ERROR: Custom section '{title}' missing 'file'")
        file_path = repo_root / file_rel
        if not file_path.exists():
            sys.exit(f"ERROR: Custom section file not found: {file_path}")
        raw = file_path.read_text().rstrip()
        body = render_string(raw, template_vars, source_name=f"custom section '{title}' ({file_rel})")
        sections.append({"title": title, "body": body})
    return sections


def render_output(
    guidelines_dir: Path,
    config: dict,
    intro: str,
    rendered_sections: list[str],
    custom_sections: list[dict],
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
        custom_sections=custom_sections,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate CONTRIBUTING.md from shared guidelines and repo config."
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to the nf-dev-guidelines config file (e.g. .github/nf-dev-guidelines.yaml)",
    )
    parser.add_argument(
        "--guidelines",
        required=True,
        help="Path to the nf-dev-guidelines repository root",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Root of the consuming repository; custom section file paths are relative to this (default: CWD)",
    )
    parser.add_argument(
        "--output",
        default="CONTRIBUTING.md",
        help="Output file path (default: CONTRIBUTING.md)",
    )
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    guidelines_dir = Path(args.guidelines).resolve()
    repo_root = Path(args.repo_root).resolve()
    output_path = Path(args.output).resolve()

    if not config_path.exists():
        sys.exit(f"ERROR: Config file not found: {config_path}")
    if not guidelines_dir.is_dir():
        sys.exit(f"ERROR: Guidelines directory not found: {guidelines_dir}")
    if not repo_root.is_dir():
        sys.exit(f"ERROR: Repo root not found: {repo_root}")

    config = load_config(config_path)
    raw_vars = config.get("vars", {})
    template_vars = {k: v.strip() if isinstance(v, str) else v for k, v in raw_vars.items()}

    intro = render_string(
        config["intro"].strip(),
        template_vars,
        source_name="intro field in config",
    )

    rendered_sections = render_sections(
        section_names=config["sections"],
        sections_dir=guidelines_dir / "sections",
        template_vars=template_vars,
    )

    custom_sections = load_custom_sections(
        custom_section_defs=config.get("custom_sections", []),
        repo_root=repo_root,
        template_vars=template_vars,
    )

    output = render_output(guidelines_dir, config, intro, rendered_sections, custom_sections)
    output = re.sub(r"\n{3,}", "\n\n", output).rstrip("\n") + "\n"
    output_path.write_text(output)
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
