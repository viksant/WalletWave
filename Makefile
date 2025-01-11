# Virtual env directory
VENV_DIR = .venv
PYTHON = python3
PIP = $(VENV_DIR)/bin/pip
ACTIVATE = source $(VENV_DIR)/bin/activate

#help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make venv	- Create the virtual environment"
	@echo "  make install	- Install Python dependencies"
	@echo "  make start	- Start the virtual environment"
	@echo "  make clean	- Remove virtual environment and temp files"

# Create virtual env
.PHONY: venv
venv:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)."

# Install requirements
.PHONY: install
install: venv
	@echo "Installing requirements..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "Requirements installed."

# Start virtual environment
.PHONY: start
start: venv
	@echo "Starting virtual environment..."
	@echo "Run 'source $(VENV_DIR)/bin/activate' to activate."

# clean up files
.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -r $(VENV_DIR)
	@echo "Virtual environment and temp files removed."
