# Installation Checklist - MCP Data Lake Agent

Use this checklist to ensure proper installation and setup.

---

## Pre-Installation

- [ ] Python 3.8+ installed
  - Verify: `python --version` or `python3 --version`
- [ ] Git installed (for cloning repository)
  - Verify: `git --version`
- [ ] OpenAI account created
  - Sign up at: https://platform.openai.com/signup
- [ ] OpenAI API key obtained
  - Get key at: https://platform.openai.com/api-keys

---

## Installation Steps

- [ ] Repository cloned
  ```bash
  git clone https://github.com/daredevilx616/MCPDataLakeAgent.git
  ```

- [ ] Changed to project directory
  ```bash
  cd MCPDataLakeAgent
  ```

- [ ] Dependencies installed
  ```bash
  pip install -r requirements.txt
  ```
  Expected packages: openai, mcp, flask, python-dotenv

- [ ] `.env` file created from example
  ```bash
  # Windows
  copy .env.example .env

  # macOS/Linux
  cp .env.example .env
  ```

- [ ] OpenAI API key added to `.env`
  ```env
  OPENAI_API_KEY=sk-your-actual-key-here
  OPENAI_MODEL=gpt-4o-mini
  ```

---

## Verification Steps

- [ ] Database file exists
  ```bash
  # Windows
  dir data\sales.db

  # macOS/Linux
  ls -l data/sales.db
  ```

- [ ] All required files present
  - [ ] `src/web_app.py`
  - [ ] `src/mcp_server.py`
  - [ ] `src/agent_core.py`
  - [ ] `templates/index.html`
  - [ ] `data/sales.db`
  - [ ] `mcp.json`
  - [ ] `.env`

- [ ] Dependencies installed correctly
  ```bash
  pip list | grep -E "openai|mcp|flask|dotenv"
  ```

---

## First Run

- [ ] Web application starts without errors
  ```bash
  python src/web_app.py
  ```

- [ ] Expected output appears
  ```
  * Running on http://127.0.0.1:5000
  * Debugger is active!
  ```

- [ ] No error messages in terminal

- [ ] Browser opens to http://localhost:5000

- [ ] Web page loads successfully
  - [ ] "Analytics Copilot" title visible
  - [ ] Chat input box visible
  - [ ] Menu button (☰) visible

---

## Functionality Test

- [ ] Test basic query
  - Type: "Show me all customers"
  - Press Enter or click Send

- [ ] Response received
  - [ ] Rationale displayed
  - [ ] SQL query shown
  - [ ] Results table appears
  - [ ] No error messages

- [ ] Database connector accessible
  - [ ] Click menu button (☰)
  - [ ] Connector panel slides in
  - [ ] SQLite path shows: `./data/sales.db`

- [ ] Test analytical query
  - Type: "What are the top 5 products by revenue?"
  - Verify results display correctly

---

## Common Issues Checklist

If you encounter problems, check:

- [ ] Python version is 3.8 or higher
- [ ] All dependencies installed successfully
- [ ] `.env` file exists in project root
- [ ] API key in `.env` has no extra spaces or quotes
- [ ] Port 5000 is not being used by another application
- [ ] Internet connection is active (required for OpenAI API)
- [ ] OpenAI account has available credits
- [ ] Current directory is project root (MCPDataLakeAgent)
- [ ] No firewall blocking Python

---

## Advanced Tests (Optional)

- [ ] MCP server runs independently
  ```bash
  python src/mcp_server.py
  ```

- [ ] Different database types can be configured
  - [ ] PostgreSQL connector form loads
  - [ ] MySQL connector form loads
  - [ ] MS SQL connector form loads
  - [ ] MongoDB connector form loads

- [ ] Complex queries work
  - Try: "Show me average order value per customer"
  - Try: "What is the monthly revenue trend?"

---

## Documentation Review

- [ ] README.md reviewed
- [ ] USER_MANUAL.md available for reference
- [ ] TROUBLESHOOTING.md accessible for issues
- [ ] QUICK_START.md available for rapid setup

---

## Submission Readiness

- [ ] All features working correctly
- [ ] No errors in console/terminal
- [ ] Sample queries execute successfully
- [ ] Documentation complete and accessible
- [ ] Project ready for demonstration

---

## Support Resources

If you checked all boxes but still have issues:

1. **Review Error Messages**
   - Check terminal/console output
   - Check browser console (F12)

2. **Consult Documentation**
   - See TROUBLESHOOTING.md for specific errors
   - See USER_MANUAL.md for detailed setup

3. **Get Help**
   - GitHub Issues: https://github.com/daredevilx616/MCPDataLakeAgent/issues
   - Include error messages and checklist status

---

**Installation Complete!** ✓

Once all boxes are checked, your MCP Data Lake Agent is ready to use.
