.PHONY: generate generate-full generate-golden preview install

GUIDELINES := .
CONFIG      := .github/test-config.yaml
CONFIG_FULL := .github/test-config-full.yaml
GOLDEN      := .github/expected-output.md
OUTPUT      := /tmp/CONTRIBUTING_preview.md

install:
	pip install -r requirements.txt

generate:
	python generator/generate.py --config $(CONFIG) --guidelines $(GUIDELINES) --output $(OUTPUT)
	@echo "Output written to $(OUTPUT)"

generate-full:
	python generator/generate.py --config $(CONFIG_FULL) --guidelines $(GUIDELINES) --output /tmp/CONTRIBUTING_preview_full.md
	@echo "Output written to /tmp/CONTRIBUTING_preview_full.md"

generate-golden:
	python generator/generate.py --config $(CONFIG) --guidelines $(GUIDELINES) --output $(GOLDEN)
	@echo "Golden file updated at $(GOLDEN)"

preview: generate
	cat $(OUTPUT)
