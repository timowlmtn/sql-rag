run-client:
	python agent/client/MCPClient.py agent/bash/run_query_agent.sh

install_python:
	@echo "Installing Python $(PYTHON_VERSION)..."
	@$(PYTHON_INSTALL_CMD)
	@echo "Python $(PYTHON_VERSION) installed."

create_venv:
	@echo "Creating virtual environment '$(VENV_NAME)'..."
	@python$(PYTHON_VERSION) -m venv $(VENV_NAME)
	@echo "Virtual environment '$(VENV_NAME)' created."

install_deps:
	@echo "Installing dependencies..."
	@$(VENV_NAME)/bin/pip install --upgrade pip
	@$(VENV_NAME)/bin/pip install -r agent/requirements.txt
	python -c "from mcp.server.fastmcp import FastMCP; print('FastMCP is installed and ready to use!')"

	@echo "Dependencies installed."
