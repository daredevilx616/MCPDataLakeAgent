# MCP Data Lake Agent - User Manual

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Using the Web Interface](#using-the-web-interface)
7. [Using the MCP Server](#using-the-mcp-server)
8. [Sample Queries](#sample-queries)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The **MCP Data Lake Agent** is an AI-powered analytics copilot that allows users to query databases using natural language. It combines:
- **Model Context Protocol (MCP)** server for database operations
- **OpenAI GPT** for natural language to SQL translation
- **Web-based chat interface** for interactive queries
- **Multi-database support** (SQLite, PostgreSQL, MySQL, MS SQL, MongoDB)

The project includes a sample SQLite database with sales data (customers, products, orders, payments) to demonstrate functionality.

---

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB free space
- **Internet Connection**: Required for OpenAI API calls

### Required Accounts
- **OpenAI API Key**: You'll need an active OpenAI account with API access
  - Sign up at: https://platform.openai.com/signup
  - Generate API key at: https://platform.openai.com/api-keys
  - Note: API usage is billed by OpenAI

---

## Installation Guide

### Step 1: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/daredevilx616/MCPDataLakeAgent.git

# Navigate to project directory
cd MCPDataLakeAgent
```

### Step 2: Verify Python Installation

```bash
# Check Python version (should be 3.8+)
python --version
# OR on some systems:
python3 --version
```

If Python is not installed:
- **Windows**: Download from https://www.python.org/downloads/
- **macOS**: Use `brew install python3` or download from python.org
- **Linux**: Use `sudo apt-get install python3` (Ubuntu/Debian)

### Step 3: Install Dependencies

**Option A: Using pip (Recommended)**
```bash
# Install all required packages
pip install -r requirements.txt

# OR if you have multiple Python versions:
python3 -m pip install -r requirements.txt
```

**Option B: Manual Installation**
```bash
pip install openai mcp flask python-dotenv
```

**Note for Linux/macOS users**: If you encounter permission issues, use:
```bash
python3 -m pip install --user -r requirements.txt
```

---

## Configuration

### Step 1: Set Up Environment Variables

1. **Copy the example environment file:**
   ```bash
   # Windows (Command Prompt)
   copy .env.example .env

   # Windows (PowerShell)
   Copy-Item .env.example .env

   # macOS/Linux
   cp .env.example .env
   ```

2. **Edit the `.env` file:**
   Open `.env` in any text editor and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=sk-your-actual-api-key-here
   OPENAI_MODEL=gpt-4o-mini
   ```

   **Where to find your API key:**
   - Log in to https://platform.openai.com/
   - Navigate to API Keys section
   - Click "Create new secret key"
   - Copy the key and paste it in the `.env` file

### Step 2: Verify Database Path

The default SQLite database is located at `./data/sales.db`. This path is pre-configured in:
- `mcp.json` - MCP server configuration
- `connectors.json` - Web UI configuration

**No changes needed** unless you want to use a different database location.

---

## Running the Application

### Method 1: Web Interface (Recommended for Beginners)

1. **Start the Flask web server:**
   ```bash
   python src/web_app.py
   # OR
   python3 src/web_app.py
   ```

2. **Expected output:**
   ```
   * Running on http://127.0.0.1:5000
   * Restarting with stat
   * Debugger is active!
   ```

3. **Open your web browser:**
   - Navigate to: `http://127.0.0.1:5000`
   - OR: `http://localhost:5000`

4. **Stop the server:**
   - Press `Ctrl+C` in the terminal

### Method 2: MCP Server (For Advanced Users)

The MCP server provides programmatic access for MCP-compatible clients.

1. **Start the MCP server:**
   ```bash
   python src/mcp_server.py
   # OR
   python3 src/mcp_server.py
   ```

2. **Configure your MCP client:**
   Point your MCP-compatible IDE or tool to the `mcp.json` configuration file in the project root.

3. **Available MCP tools:**
   - `describe_schema()` - Get database schema information
   - `run_sql(query)` - Execute read-only SELECT queries
   - `create_table(schema_sql)` - Create new tables
   - `insert_row(table, values)` - Insert a single row
   - `update_rows(table, updates, where_clause, params)` - Update rows
   - `delete_rows(table, where_clause, params)` - Delete rows

---

## Using the Web Interface

### Interface Overview

The web interface has three main sections:

1. **Navigation Rail (Left)**: Toggle button for database connectors
2. **Connector Panel (Sidebar)**: Configure database connections
3. **Chat Panel (Main)**: Interact with the AI agent

### Configuring Database Connectors

1. **Click the menu button (☰)** in the navigation rail to open connectors
2. **Select Active Database** from the dropdown:
   - SQLite (default)
   - PostgreSQL
   - MySQL
   - MS SQL Server
   - MongoDB

3. **Configure connection details:**
   - Expand the connector card for your chosen database
   - Fill in connection details (host, port, credentials, etc.)
   - Click **Save** button

4. **SQLite Configuration** (Default):
   - Database Path: `./data/sales.db`
   - No additional configuration needed

### Asking Questions

1. **Type your question** in the chat input box at the bottom
2. **Examples:**
   - "Show me all customers"
   - "What are the top 5 products by revenue?"
   - "How many orders were placed last month?"
   - "What is the average order value?"

3. **Press Enter** or click **Send**

4. **Review the response:**
   - **Rationale**: Explanation of the approach
   - **Generated SQL**: The query created by the AI
   - **Results**: Data displayed in a table format

### Understanding the Response

Each response includes:
- **Rationale**: Why the AI chose this approach
- **SQL Query**: The actual SQL generated
- **Result Table**: Query results displayed in tabular format
- **Row Count**: Number of rows returned

---

## Using the MCP Server

### Setup for IDE Integration

1. **Ensure `mcp.json` is in your project root**
2. **Configure your MCP-compatible tool** to use this configuration
3. **Common MCP clients:**
   - Claude Desktop App
   - VS Code with MCP extension
   - Custom applications using MCP SDK

### Direct Tool Usage

The MCP server exposes the following tools:

#### 1. Describe Schema
```json
{
  "tool": "describe_schema",
  "arguments": {}
}
```
Returns list of tables and columns.

#### 2. Run SQL Query
```json
{
  "tool": "run_sql",
  "arguments": {
    "query": "SELECT * FROM customers LIMIT 10"
  }
}
```
Executes read-only queries.

#### 3. Create Table
```json
{
  "tool": "create_table",
  "arguments": {
    "schema_sql": "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
  }
}
```

#### 4. Insert Row
```json
{
  "tool": "insert_row",
  "arguments": {
    "table": "customers",
    "values": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

---

## Sample Queries

### Basic Queries

**List all tables:**
```
What tables are in the database?
```

**View customer data:**
```
Show me the first 10 customers
```

**Count records:**
```
How many products do we have?
```

### Analytical Queries

**Revenue analysis:**
```
What is the total revenue from all orders?
```

**Top performers:**
```
Show me the top 5 customers by total spending
```

**Trend analysis:**
```
What is the monthly revenue trend?
```

### Complex Queries

**Join queries:**
```
Show me customer names with their order counts
```

**Aggregations:**
```
What is the average order value per customer?
```

**Filters:**
```
Show me orders above $1000 in the last 30 days
```

---

## Troubleshooting

### Common Issues

#### 1. "OPENAI_API_KEY is not set" Error

**Solution:**
- Ensure `.env` file exists in the project root
- Verify the API key is correctly set in `.env`
- Check for extra spaces or quotes around the key
- Restart the application after editing `.env`

#### 2. "Module not found" Error

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# OR use pip3
pip3 install -r requirements.txt
```

#### 3. Port 5000 Already in Use

**Solution:**
- Stop other applications using port 5000
- OR modify `src/web_app.py` line 160 to use a different port:
  ```python
  app.run(debug=True, port=5001)
  ```

#### 4. Database File Not Found

**Solution:**
- Verify `data/sales.db` exists in the project directory
- Check the path in `mcp.json` and `connectors.json`
- Ensure you're running the application from the project root

#### 5. OpenAI API Rate Limit Error

**Solution:**
- Wait a few seconds before sending another query
- Check your OpenAI account billing and usage limits
- Consider upgrading your OpenAI plan

#### 6. Cannot Connect to Database

**For SQLite:**
- Verify file path is correct
- Ensure you have read permissions

**For PostgreSQL/MySQL/MS SQL:**
- Verify host, port, and credentials
- Ensure database server is running
- Check firewall settings
- Test connection using database client first

### Getting Help

If you encounter issues not covered here:

1. **Check the console/terminal** for detailed error messages
2. **Review the logs** for debugging information
3. **Verify all configuration files** are properly set up
4. **Test with the sample SQLite database** first before using custom databases
5. **Create an issue** on GitHub: https://github.com/daredevilx616/MCPDataLakeAgent/issues

---

## Advanced Configuration

### Using Custom Databases

1. **Prepare your database:**
   - Ensure it's accessible from your machine
   - Note connection details (host, port, credentials)

2. **Configure in Web UI:**
   - Open the connector panel
   - Select your database type
   - Fill in connection details
   - Click Save

3. **Update MCP configuration** (optional):
   - Edit `mcp.json` to add environment variables
   - Modify `src/mcp_server.py` if needed for custom logic

### Changing AI Model

Edit `.env` file:
```env
OPENAI_MODEL=gpt-4  # For more accurate results (higher cost)
OPENAI_MODEL=gpt-4o-mini  # For cost-effective queries (default)
OPENAI_MODEL=gpt-3.5-turbo  # For fastest responses
```

### Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use environment variables** for sensitive data
3. **Restrict database permissions** to read-only when possible
4. **Use strong passwords** for database connections
5. **Enable HTTPS** in production deployments
6. **Rotate API keys** regularly

---

## Project Structure

```
MCPDataLakeAgent/
├── data/
│   └── sales.db              # Sample SQLite database
├── src/
│   ├── agent_core.py         # Core AI agent logic
│   ├── mcp_server.py         # MCP server implementation
│   └── web_app.py            # Flask web application
├── templates/
│   └── index.html            # Web UI template
├── .env                      # Environment variables (create from .env.example)
├── .env.example              # Example environment file
├── .gitignore                # Git ignore rules
├── connectors.json           # Database connector config
├── mcp.json                  # MCP server config
├── README.md                 # Quick start guide
├── requirements.txt          # Python dependencies
└── USER_MANUAL.md            # This file
```

---

## Support and Contact

- **GitHub Repository**: https://github.com/daredevilx616/MCPDataLakeAgent
- **Issues**: https://github.com/daredevilx616/MCPDataLakeAgent/issues
- **Documentation**: See README.md for quick start

---

## License

This project is provided for educational purposes. Please refer to the LICENSE file for details.

---

**Last Updated**: December 2024
**Version**: 1.0
