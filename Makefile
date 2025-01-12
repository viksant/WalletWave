# Virtual env directory
VENV_DIR = .venv
PYTHON = python3
PIP = $(VENV_DIR)/bin/pip
ACTIVATE = source $(VENV_DIR)/bin/activate
PACKAGE_NAME = WalletWave

#help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install     		- Create a virtual environment and install dependencies"
	@echo "  make uninstall         - Uninstall WalletWave and its dependencies"
	@echo "  make build             - Build the package"
	@echo "  make clean             - Remove virtual environment and build artifacts"


.PHONY: install
install: venv
	@echo "Installing dependencies in virtual environment..."
	@$(PIP) install --upgrade pip
	@$(PIP) install .
	@echo "Dependencies installed in virtual environment."
	@echo "To run the package, activate the virtual environment:"
		@if [ "$(OS)" = "Windows_NT" ]; then \
		echo "Use: .venv\\Scripts\\Activate.ps1 (PowerShell) or .venv\\Scripts\\activate.bat (Command Prompt)"; \
	else \
		echo "Use: source $(VENV_DIR)/bin/activate"; \
	fi
	@echo "Then run: walletwave"

# Create virtual environment
.PHONY: venv
venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
		echo "Virtual environment created in $(VENV_DIR)."; \
	else \
		echo "Virtual environment already exists in $(VENV_DIR)."; \
	fi

# Uninstall WalletWave and its dependencies
.PHONY: uninstall
uninstall:
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Uninstalling WalletWave and its dependencies from virtual environment..."; \
		$(VENV_DIR)/bin/pip uninstall -y $(PACKAGE_NAME); \
		$(VENV_DIR)/bin/pip freeze | while read pkg; do $(VENV_DIR)/bin/pip uninstall -y $$pkg; done; \
		echo "Uninstallation complete for virtual environment."; \
	else \
		echo "Uninstalling WalletWave and its dependencies globally..."; \
		$(PYTHON) -m pip uninstall -y $(PACKAGE_NAME); \
		$(PYTHON) -m pip freeze | while read pkg; do $(PYTHON) -m pip uninstall -y $$pkg; done; \
		echo "Uninstallation complete globally."; \
	fi

# Build the package
.PHONY: build
build: venv
	@echo "Ensuring 'build' module is installed in the virtual environment..."
	@$(PIP) install --upgrade build
	@echo "Building the package..."
	@$(VENV_DIR)/bin/python -m build
	@echo "Build complete."

# clean up files
.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR) dist build *.egg-info
	@echo "Cleanup complete."
