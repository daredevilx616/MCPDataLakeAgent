# Troubleshooting Guide - MCP Data Lake Agent

This guide helps you diagnose and fix common issues when installing or running the MCP Data Lake Agent.

---

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Configuration Issues](#configuration-issues)
3. [Runtime Errors](#runtime-errors)
4. [Database Connection Issues](#database-connection-issues)
5. [API and Authentication Issues](#api-and-authentication-issues)
6. [Performance Issues](#performance-issues)
7. [Web Interface Issues](#web-interface-issues)

---

## Installation Issues

### Issue: "Python not found" or "python is not recognized"

**Symptoms:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your terminal/command prompt
4. Verify: `python --version`

**macOS:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3

# Verify
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
python3 --version
```

---

### Issue: "pip install" fails with permission error

**Symptoms:**
```
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied
```

**Solutions:**

**Option 1: Install for current user only**
```bash
pip install --user -r requirements.txt
```

**Option 2: Use virtual environment (recommended)**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Option 3: Use administrator/sudo (not recommended)**
```bash
# Windows (run as administrator)
pip install -r requirements.txt

# macOS/Linux
sudo pip3 install -r requirements.txt
```

---

### Issue: "No module named 'mcp'" or other import errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'mcp'
ModuleNotFoundError: No module named 'openai'
```

**Solutions:**

1. **Verify pip installation:**
```bash
pip list
```
Check if `mcp`, `openai`, `flask`, and `python-dotenv` are listed.

2. **Reinstall dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

3. **Check Python version:**
```bash
python --version  # Should be 3.8 or higher
```

4. **Use correct Python executable:**
```bash
# If you have multiple Python versions
python3 -m pip install -r requirements.txt
python3 src/web_app.py
```

---

## Configuration Issues

### Issue: "OPENAI_API_KEY is not set"

**Symptoms:**
```
RuntimeError: OPENAI_API_KEY is not set. Define it in the environment or .env file.
```

**Solutions:**

1. **Verify .env file exists:**
```bash
# Windows
dir .env

# macOS/Linux
ls -la .env
```

2. **Create .env from example:**
```bash
# Windows (Command Prompt)
copy .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env

# macOS/Linux
cp .env.example .env
```

3. **Edit .env file:**
Open `.env` in a text editor and add:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

4. **Get OpenAI API key:**
   - Visit: https://platform.openai.com/api-keys
   - Sign up or log in
   - Click "Create new secret key"
   - Copy the key (starts with "sk-")
   - Paste into `.env` file

5. **Verify no extra spaces:**
```env
# Correct
OPENAI_API_KEY=sk-abc123

# Incorrect (has spaces)
OPENAI_API_KEY = sk-abc123
OPENAI_API_KEY=sk-abc123
```

6. **Restart the application** after editing `.env`

---

### Issue: Database path not found

**Symptoms:**
```
sqlite3.OperationalError: unable to open database file
```

**Solutions:**

1. **Verify database exists:**
```bash
# Windows
dir data\sales.db

# macOS/Linux
ls -l data/sales.db
```

2. **Check current directory:**
```bash
# Windows
cd

# macOS/Linux
pwd
```
Make sure you're in the project root directory (MCPDataLakeAgent).

3. **Verify path in configuration:**
Open `mcp.json` and check:
```json
{
  "mcpServers": {
    "analytics-sqlite": {
      "env": {
        "MCP_DB_PATH": "./data/sales.db"
      }
    }
  }
}
```

4. **Use absolute path (if relative doesn't work):**
```json
"MCP_DB_PATH": "C:/Users/YourName/MCPDataLakeAgent/data/sales.db"
```

---

## Runtime Errors

### Issue: Port 5000 already in use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**

**Option 1: Find and kill the process using port 5000**

**Windows:**
```bash
# Find process
netstat -ano | findstr :5000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# Find process
lsof -i :5000

# Kill process (replace PID with actual number)
kill -9 <PID>
```

**Option 2: Use a different port**

Edit `src/web_app.py` (line 160):
```python
# Change from
app.run(debug=True)

# To
app.run(debug=True, port=5001)
```

Then access at: `http://localhost:5001`

---

### Issue: Application crashes with JSON decode error

**Symptoms:**
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solutions:**

1. **Check if config files are valid JSON:**
```bash
# Validate mcp.json
python -m json.tool mcp.json

# Validate connectors.json
python -m json.tool connectors.json
```

2. **Reset to default configurations:**
```bash
# Backup current files
copy mcp.json mcp.json.backup
copy connectors.json connectors.json.backup

# Delete and recreate from repository
```

3. **Check for empty or corrupted files:**
Open `mcp.json` and `connectors.json` in a text editor and verify they contain valid JSON.

---

### Issue: "Model returned empty response"

**Symptoms:**
```
RuntimeError: Model returned empty response
```

**Solutions:**

1. **Check OpenAI API status:**
   Visit: https://status.openai.com/

2. **Verify API key is valid:**
```bash
# Test API key with curl (macOS/Linux)
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

3. **Check account balance:**
   - Log in to https://platform.openai.com/account/billing
   - Verify you have available credits

4. **Try a different model:**
Edit `.env`:
```env
OPENAI_MODEL=gpt-4o-mini
# OR
OPENAI_MODEL=gpt-3.5-turbo
```

---

## Database Connection Issues

### Issue: Cannot connect to PostgreSQL/MySQL

**Symptoms:**
```
OperationalError: could not connect to server
Connection refused
```

**Solutions:**

1. **Verify database server is running:**
```bash
# PostgreSQL
sudo service postgresql status

# MySQL
sudo service mysql status
```

2. **Check connection details:**
   - Host: Usually `localhost` or `127.0.0.1`
   - Port: PostgreSQL (5432), MySQL (3306)
   - Username/Password: Must match database credentials
   - Database name: Must exist on the server

3. **Test connection separately:**
```bash
# PostgreSQL
psql -h localhost -U username -d database_name

# MySQL
mysql -h localhost -u username -p database_name
```

4. **Check firewall settings:**
Ensure firewall allows connections on database port.

5. **Verify database drivers are installed:**
```bash
# PostgreSQL
pip install psycopg2-binary

# MySQL
pip install mysql-connector-python
```

---

### Issue: SQLite database is locked

**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Solutions:**

1. **Close other applications** accessing the database
2. **Stop the web app and MCP server**, then restart
3. **Check for stale lock files:**
```bash
# macOS/Linux
rm data/sales.db-journal
```

4. **Wait a few seconds** and try again

---

## API and Authentication Issues

### Issue: OpenAI rate limit exceeded

**Symptoms:**
```
RateLimitError: Rate limit reached for requests
```

**Solutions:**

1. **Wait before sending another request** (usually 60 seconds)
2. **Check your usage limits:**
   - Free tier: Lower rate limits
   - Paid tier: Higher rate limits
3. **Upgrade your OpenAI plan** if needed
4. **Implement request throttling** (add delays between queries)

---

### Issue: Invalid API key format

**Symptoms:**
```
AuthenticationError: Incorrect API key provided
```

**Solutions:**

1. **Verify API key format:**
   - Should start with `sk-`
   - Should be around 48-51 characters long
   - No spaces or quotes around it

2. **Check for common mistakes:**
```env
# Correct
OPENAI_API_KEY=sk-abc123xyz789

# Incorrect
OPENAI_API_KEY="sk-abc123xyz789"  # No quotes
OPENAI_API_KEY='sk-abc123xyz789'  # No quotes
OPENAI_API_KEY=sk-abc123xyz789    # No trailing space
```

3. **Regenerate API key:**
   - Go to https://platform.openai.com/api-keys
   - Delete old key
   - Create new key
   - Update `.env` file

---

## Performance Issues

### Issue: Slow query responses

**Symptoms:**
- Application takes 10+ seconds to respond
- Queries timeout

**Solutions:**

1. **Check internet connection** (API calls require internet)
2. **Use faster model:**
```env
OPENAI_MODEL=gpt-3.5-turbo  # Faster than gpt-4
```

3. **Simplify your question:**
   - Instead of: "Give me a detailed analysis of revenue trends over the last 5 years broken down by product category with growth percentages"
   - Try: "Show revenue by product category"

4. **Check OpenAI API status:**
   Visit: https://status.openai.com/

5. **Optimize database:**
```sql
-- Create indexes on frequently queried columns
CREATE INDEX idx_customer_id ON orders(customer_id);
CREATE INDEX idx_order_date ON orders(order_date);
```

---

### Issue: High memory usage

**Symptoms:**
- System runs slow
- Application crashes with memory error

**Solutions:**

1. **Limit result set size:**
   Ask for: "Show me the top 10 customers" instead of "Show me all customers"

2. **Close unused applications**

3. **Increase available memory:**
   - Close browser tabs
   - Restart computer

4. **Use pagination in queries:**
```sql
SELECT * FROM orders LIMIT 100 OFFSET 0
```

---

## Web Interface Issues

### Issue: Webpage doesn't load

**Symptoms:**
- Browser shows "This site can't be reached"
- Connection refused error

**Solutions:**

1. **Verify application is running:**
   Check terminal for:
   ```
   * Running on http://127.0.0.1:5000
   ```

2. **Check correct URL:**
   - Try: `http://localhost:5000`
   - Try: `http://127.0.0.1:5000`
   - NOT: `https://` (no SSL)

3. **Clear browser cache:**
   - Ctrl+Shift+Delete (Windows/Linux)
   - Cmd+Shift+Delete (macOS)

4. **Try different browser:**
   Test with Chrome, Firefox, Edge, or Safari

5. **Check firewall:**
   Allow Python through firewall

---

### Issue: Chat doesn't respond to questions

**Symptoms:**
- Click "Send" but nothing happens
- Error message appears in chat

**Solutions:**

1. **Check browser console for errors:**
   - Press F12
   - Go to Console tab
   - Look for error messages

2. **Verify backend is running:**
   Check terminal for any error messages

3. **Test API endpoint directly:**
```bash
# Using curl (macOS/Linux)
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show all customers"}'
```

4. **Check network tab:**
   - Press F12
   - Go to Network tab
   - Send a question
   - Check if `/api/query` request appears

---

### Issue: Database connector changes don't save

**Symptoms:**
- Click "Save" but settings revert
- Error message appears

**Solutions:**

1. **Check file permissions:**
```bash
# macOS/Linux
chmod 644 connectors.json
chmod 644 mcp.json
```

2. **Verify files exist and are writable:**
```bash
ls -l *.json
```

3. **Check for file locks:**
   Close any text editors that have the JSON files open

4. **Restart the application:**
   Stop (Ctrl+C) and restart `python src/web_app.py`

---

## Advanced Troubleshooting

### Enable Debug Mode

Edit `src/web_app.py` to see more detailed error messages:
```python
# Already enabled by default at line 160
app.run(debug=True)
```

### Check Logs

Look at terminal output for detailed error messages:
```
* Running on http://127.0.0.1:5000
[error messages will appear here]
```

### Verify All Dependencies

```bash
pip list | grep -E "openai|mcp|flask|dotenv"
```

Expected output:
```
Flask           3.0.0
mcp             0.9.0
openai          1.3.0
python-dotenv   1.0.0
```

### Test Database Connection

```python
# Create test file: test_db.py
import sqlite3
conn = sqlite3.connect('./data/sales.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())
conn.close()
```

Run:
```bash
python test_db.py
```

---

## Getting Additional Help

If you've tried all solutions and still have issues:

1. **Collect error information:**
   - Full error message from terminal
   - Python version: `python --version`
   - OS version
   - Steps to reproduce the error

2. **Create a GitHub issue:**
   - Go to: https://github.com/daredevilx616/MCPDataLakeAgent/issues
   - Click "New Issue"
   - Provide all error information

3. **Check existing issues:**
   - Someone may have already reported the same problem
   - Search: https://github.com/daredevilx616/MCPDataLakeAgent/issues

---

## Quick Diagnostic Checklist

Before reporting an issue, verify:

- [ ] Python 3.8+ is installed
- [ ] All dependencies are installed (`pip list`)
- [ ] `.env` file exists and contains valid API key
- [ ] Application is running (check terminal)
- [ ] Database file exists (`data/sales.db`)
- [ ] Port 5000 is not in use by another app
- [ ] Correct URL in browser (`http://localhost:5000`)
- [ ] Internet connection is active
- [ ] OpenAI API is operational
- [ ] Browser console shows no errors (F12)

---

**Last Updated**: December 2024
