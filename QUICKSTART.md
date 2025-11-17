# Quick Start Guide

## Step-by-Step Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 3. Create Database
```bash
python database_setup.py
```

Expected output:
```
Database created successfully!
- Customers: 100
- Products: 20
- Orders: 600
- Order Items: 1500
```

### 4. Verify Setup (Optional)
```bash
python setup_check.py
```

### 5. Run Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## First Steps

1. **Explore the Dashboard**
   - View key business metrics
   - Check out the charts and visualizations
   - Review top products and revenue trends

2. **Try the Chat Interface**
   - Click on the "💬 Chat with Agent" tab
   - Ask a question like: "Show me the top 5 customers by revenue"
   - Watch the agent use function calling to query the database

3. **Test Safety Features**
   - Try asking: "Delete all customers"
   - The agent will refuse and explain why

4. **Create a Support Ticket**
   - Use the sidebar to create a test ticket
   - Configure your GitHub/Trello/Jira credentials in .env if needed

## Example Queries

Try these queries in the chat interface:

- "What are the top 10 best selling products?"
- "Show me customers from New York"
- "What is the total revenue for completed orders?"
- "Which city has the most customers?"
- "Show me orders from the last month"
- "What products are in the Electronics category?"

## Troubleshooting

**Database not found error:**
- Run `python database_setup.py` again

**OpenAI API errors:**
- Check your API key in `.env`
- Verify you have GPT-4 access
- Check your account has credits

**Import errors:**
- Run `pip install -r requirements.txt` again
- Make sure you're using Python 3.8+

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the code in `agent.py` to understand function calling
- Customize the dashboard in `app.py`
- Add more sample queries or features

