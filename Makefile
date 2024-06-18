# Define the virtual environment directory
VENV_DIR := .venv

# Define the Python executable within the virtual environment
PYTHON := $(VENV_DIR)/Scripts/python

# Default target: create the virtual environment and install dependencies
all: $(VENV_DIR) requirements.txt
	$(PYTHON) -m pip install -r requirements.txt

# Target to create the virtual environment
$(VENV_DIR):
	python -m venv $(VENV_DIR)

# Target to run your main script (replace main.py with your actual script)
run: $(VENV_DIR) requirements.txt
	$(PYTHON) main.py

# Target to clean the virtual environment
clean:
	rm -rf $(VENV_DIR)
