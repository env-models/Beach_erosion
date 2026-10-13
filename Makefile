# Shortcuts for the commands documented in README.md ("How to reproduce").
# Every target only wraps existing entry points; `make -n <target>` prints the commands without running them.
# Re-running tables/audit/models/report overwrites committed results (frozen, DECISIONS D-30): check `git diff`.

PY ?= .venv/bin/python
# Data versions for `make models`: with figures, then without (slope-fix sensitivity). v2C also needs raw tide netCDF.
DATA ?= v1 v2
DATA_NOFIGS ?= v1s v2s
REPORT_TAGS ?= v1 v2 v2C

.PHONY: help env test tables audit models report download process

help:
	@echo "make env       create .venv (Python 3.12, uv) and install the locked environment + package evi"
	@echo "make test      pytest -q (24 tests; tests/review_*.py not collected)"
	@echo "make tables    rebuild event/interval tables v1, v2 and *_slopefix in data/processed/"
	@echo "make audit     reproduction/audit numbers (reports/A_audit.md section 1) -> data/processed/reproduction_A.json"
	@echo "make models    run the Agent C pipeline on DATA=\"$(DATA)\" (+ DATA_NOFIGS=\"$(DATA_NOFIGS)\" without figures)"
	@echo "make report    refresh auto tables in reports/C_models.md and reports/C_model_cards/"
	@echo "make download  fetch external raw data into data/raw/ (network; see scripts/README.md)"
	@echo "make process   turn data/raw/ into data/processed/ (waves, tides, surveys, climate indices)"

env:
	uv venv --python 3.12 .venv
	uv pip install --python $(PY) -r requirements.lock.txt
	# requirements.txt adds anything missing from the lock file (e.g. utide); satisfied pins are kept
	uv pip install --python $(PY) -r requirements.txt
	uv pip install --python $(PY) -e .

test:
	$(PY) -m pytest -q

tables:
	$(PY) -m evi.events
	$(PY) -m evi.events_v2
	$(PY) -m evi.slopefix

audit:
	$(PY) -m evi.reproduce

models:
	for d in $(DATA); do $(PY) -m evi.models.run_all --data $$d || exit 1; done
	for d in $(DATA_NOFIGS); do $(PY) -m evi.models.run_all --data $$d --no-figs || exit 1; done
	$(PY) -c "from evi.models.run_all import hat_sensitivity, direction_ablation; hat_sensitivity(); direction_ablation()"

report:
	$(PY) -m evi.models.report $(REPORT_TAGS)

download:
	$(PY) -I scripts/download_castelle2020.py
	$(PY) -I scripts/download_resourcecode.py
	$(PY) -I scripts/download_shom_tidegauges.py
	$(PY) -I scripts/download_shom_ram.py
	$(PY) -I scripts/download_climate_indices.py

process:
	$(PY) -I scripts/process_castelle2020.py
	$(PY) -I scripts/process_waves.py
	$(PY) -I scripts/process_tide.py
	$(PY) -I scripts/process_climate_indices.py
