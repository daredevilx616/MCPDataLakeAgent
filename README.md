# MCP Data Lake Agent

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT-green.svg)](https://openai.com/)

> An AI-powered natural language database query system using OpenAI GPT and Model Context Protocol (MCP)

**MCP Data Lake Agent** is an intelligent analytics copilot that translates natural language questions into SQL queries, executes them, and presents results in a beautiful web interface. No SQL knowledge required!

---

## Features

- **Natural Language Queries**: Ask questions in plain English, get SQL results
- **Multi-Database Support**: SQLite, PostgreSQL, MySQL, MS SQL Server, MongoDB
- **Web Chat Interface**: Clean, dark-themed UI for interactive analytics
- **MCP Server**: Exposes database tools via Model Context Protocol
- **Sample Database**: Pre-loaded sales data for immediate testing
- **Real-time Results**: See generated SQL, rationale, and tabular data
- **CRUD Operations**: Create, read, update, and delete database records

---

## Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/daredevilx616/MCPDataLakeAgent.git
cd MCPDataLakeAgent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env

# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
# OPENAI_MODEL=gpt-4o-mini

# 4. Launch the web application
python src/web_app.py

# 5. Open your browser to http://localhost:5000
```

**That's it!** You can now start asking questions about the sample sales database.

---

## Usage Examples

Try these sample questions in the web interface:

```
Show me all customers
What are the top 5 products by revenue?
How many orders were placed last month?
What is the average order value?
Show me revenue by product category
```

The AI will:
1. Understand your question
2. Generate appropriate SQL
3. Execute the query
4. Display results in a formatted table

---

## Project Structure

```
MCPDataLakeAgent/
├── src/
│   ├── agent_core.py         # AI agent & SQL generation
│   ├── mcp_server.py         # MCP protocol server
│   └── web_app.py            # Flask web application
├── templates/
│   └── index.html            # Web UI
├── data/
│   └── sales.db              # Sample SQLite database
├── .env.example              # Environment template
├── requirements.txt          # Python dependencies
├── mcp.json                  # MCP server configuration
├── connectors.json           # Database connectors
├── README.md                 # This file
├── USER_MANUAL.md            # Detailed documentation
├── TROUBLESHOOTING.md        # Common issues & solutions
├── SUBMISSION.md             # Project overview
└── LICENSE                   # MIT License
```

---

## Documentation

- **[USER_MANUAL.md](USER_MANUAL.md)** - Complete installation and usage guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[SUBMISSION.md](SUBMISSION.md)** - Project overview and architecture

---

## Advanced Usage

### Configuration

Edit `.env` to customize:
```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini  # Or gpt-4, gpt-3.5-turbo
```

**Notes:**
- The agent reads the schema before the first call and instructs the model to return JSON with `sql` and `rationale`
- Results appear in the chat bubble with tables and multi-statement blocks
- Set `OPENAI_MODEL` to `gpt-4` for more complex queries (higher cost)

---

## Running the MCP Server

For integration with MCP-compatible tools:

```bash
# Start the MCP server
python src/mcp_server.py
```

The server defaults to stdio transport and reads database path from `mcp.json`. Configure your MCP client/IDE to use this workspace.

### Available MCP Tools

- `describe_schema()` - Returns table/column metadata for schema discovery
- `run_sql(query)` - Executes read-only SELECT/CTE statements
- `create_table(schema_sql)` - Runs DDL statements to create new tables
- `insert_row(table, values)` - Inserts a single row as a JSON object
- `update_rows(table, updates, where_clause, params)` - Updates rows with WHERE filter
- `delete_rows(table, where_clause, params)` - Deletes rows with WHERE filter

---

## Web Interface

Open `http://127.0.0.1:5000` once Flask is running. The interface includes:

- **Navigation Rail**: Toggle database connector panel
- **Connector Panel**: Multi-database configuration forms
  - SQLite, PostgreSQL, MySQL, MS SQL Server, MongoDB
  - Active database selector
- **Chat Workspace**: Interactive query interface
  - Natural language input
  - Generated SQL display
  - Rationale explanations
  - Tabular results with row counts

Connector changes are saved to `connectors.json` and synced to `mcp.json` automatically.

---

## Sample Database

The included `data/sales.db` contains:

**Tables:**
- `customers` - Customer information
- `products` - Product catalog
- `orders` - Order records
- `payments` - Payment transactions

This sample data allows immediate testing without additional database setup.

---

## Technology Stack

- **Python 3.8+**: Core programming language
- **Flask**: Web framework
- **OpenAI API**: GPT models for NL to SQL translation
- **MCP**: Model Context Protocol for AI tool integration
- **SQLite**: Embedded database (with multi-DB support)

---

## Wiring an OpenAI Agent to the MCP Server

Configure an OpenAI Models agent (Assistants API or Responses API with MCP support) and pass `mcp.json` in your IDE/tooling so the agent can call `analytics-sqlite`.

At runtime, the AI agent can:
1. Call `describe_schema` to scope available tables
2. Plan SQL via the LLM
3. Send SQL to `run_sql` to get live results
4. Answer the user with both rationale and data

This enables local iteration before deploying to production or adding additional MCP tools.

---

## Troubleshooting

Common issues and solutions:

- **"OPENAI_API_KEY is not set"**: Ensure `.env` file exists and contains valid API key
- **"Port 5000 already in use"**: Stop other services or change port in `web_app.py`
- **"Module not found"**: Run `pip install -r requirements.txt`
- **Database errors**: Verify `data/sales.db` exists and path is correct

For detailed troubleshooting, see **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

---

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [OpenAI](https://openai.com/) for GPT API
- [Anthropic](https://www.anthropic.com/) for Model Context Protocol
- [Flask](https://flask.palletsprojects.com/) community for excellent documentation

---

## Support

- **GitHub**: https://github.com/daredevilx616/MCPDataLakeAgent
- **Issues**: https://github.com/daredevilx616/MCPDataLakeAgent/issues
- **Documentation**: See [USER_MANUAL.md](USER_MANUAL.md)

---

**Built with ❤️ for data analytics and AI integration**
