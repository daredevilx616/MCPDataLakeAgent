# Quick Start Guide - MCP Data Lake Agent

**Get running in 5 minutes!**

---

## Step 1: Install Python

Ensure you have Python 3.8 or higher:
```bash
python --version
```

If not installed, download from: https://www.python.org/downloads/

---

## Step 2: Clone & Navigate

```bash
git clone https://github.com/daredevilx616/MCPDataLakeAgent.git
cd MCPDataLakeAgent
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: On Linux/macOS, you might need:
```bash
pip3 install -r requirements.txt
```

---

## Step 4: Get OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

---

## Step 5: Configure Environment

**Windows:**
```bash
copy .env.example .env
notepad .env
```

**macOS/Linux:**
```bash
cp .env.example .env
nano .env
```

Add your API key:
```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

Save and close the file.

---

## Step 6: Run the Application

```bash
python src/web_app.py
```

**Expected output:**
```
* Running on http://127.0.0.1:5000
* Debugger is active!
```

---

## Step 7: Open Browser

Navigate to: **http://localhost:5000**

---

## Step 8: Try It Out!

Type any of these questions in the chat:

```
Show me all customers
What are the top 5 products by revenue?
How many orders were placed?
What is the total revenue?
```

---

## Troubleshooting

**Can't run python?**
- Windows: Try `py` instead of `python`
- macOS/Linux: Try `python3` instead of `python`

**Module not found error?**
```bash
pip install openai mcp flask python-dotenv
```

**Port 5000 already in use?**
- Stop other apps using that port
- Or edit `src/web_app.py` line 160 to use port 5001

**API key error?**
- Make sure `.env` file exists
- Verify API key has no extra spaces
- Restart the application

---

## Next Steps

Once it's working:

- **[USER_MANUAL.md](USER_MANUAL.md)** - Full documentation
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Detailed error solutions
- **[SUBMISSION.md](SUBMISSION.md)** - Project architecture & overview

---

**Need help?**
- Check console/terminal for error messages
- See TROUBLESHOOTING.md
- Create an issue: https://github.com/daredevilx616/MCPDataLakeAgent/issues

---

**That's it! You're ready to query databases with natural language!**
