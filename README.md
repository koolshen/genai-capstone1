---
title: Stock Data Insights App
emoji: 📈
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
license: mit
---

# Stock Data Insights App

A Streamlit-based application that provides AI-powered insights from a stock market SQLite database. The app features an intelligent agent powered by Google Gemini AI that helps users query and analyze stock data using natural language, with built-in safety features to prevent dangerous database operations.

## Features

- **AI Agent with Function Calling**: Uses Google Gemini AI to intelligently understand queries and generate SQL to query the database
- **Interactive Dashboard**: Real-time stock market metrics, charts, and visualizations
- **Safety Features**: Prevents dangerous operations (DELETE, DROP, UPDATE, etc.) - read-only access
- **Support Ticket Integration**: Create support tickets in Trello
- **Console Logging**: All agent operations are logged to the console
- **Chat Interface**: Natural language interface for querying stock data
- **Stock Query Validation**: Automatically detects and warns about non-stock related queries

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- (Optional) Trello credentials for support ticket functionality

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd genai-capstone1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: For support ticket functionality
TRELLO_API_KEY=your_trello_api_key
TRELLO_TOKEN=your_trello_token
TRELLO_BOARD_ID=your_trello_board_id
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

4. Initialize the stock database:
```bash
python stock_database_setup.py
```

This will create a `stock_data.db` SQLite database with:
- 117 unique stocks
- 12 sectors (Technology, Healthcare, Financial Services, etc.)
- 11,000+ stock records with daily price data
- 90 days of historical data

5. (Optional) Verify setup:
```bash
python setup_check.py
```

This will check if all dependencies, environment variables, and database are properly configured.

### Hugging Face Spaces

To deploy this app on Hugging Face Spaces:

1. **Create a new Space** on [Hugging Face Spaces](https://huggingface.co/spaces)
   - Choose **Streamlit** as the SDK
   - Set the repository name (e.g., `stock-data-insights`)

2. **Add your API key as a Secret**:
   - Go to your Space settings
   - Navigate to "Variables and secrets"
   - Add a new secret named `GEMINI_API_KEY` with your API key value
   - (Optional) Add Trello credentials if you want support ticket functionality

3. **Push your code** to the Space:
   ```bash
   git remote add space https://huggingface.co/spaces/<username>/<space-name>
   git push space main
   ```

4. **The database will auto-initialize** on first run. The app will automatically create the stock database if it doesn't exist.

**Note**: The database initialization may take a few minutes on the first run. Be patient!

## Usage

1. Start the Streamlit application:
```bash
python -m streamlit run app.py
```

2. Open your browser to `http://localhost:8501`

3. Explore the dashboard and chat with the AI agent!

## Application Workflow

### Dashboard Tab

The dashboard provides:
- **Market Overview**: Total records, unique stocks, sectors, and latest date
- **Price Statistics**: Average, minimum, and maximum stock prices
- **Stocks by Sector**: Pie chart showing distribution of stocks across sectors
- **Top Stocks by Market Cap**: Table of largest companies by market capitalization
- **Top Gainers and Losers**: Best and worst performing stocks
- **Highest Trading Volume**: Most actively traded stocks

### Chat Tab

Interact with the AI agent using natural language. The agent understands your queries and generates appropriate SQL to retrieve stock data.

**Example Queries:**
- "Show me the top 10 stocks by market cap"
- "What are the best performing stocks today?"
- "Show me stocks from the technology sector"
- "What is the average price of stocks in the S&P 500?"
- "Show me stocks with highest trading volume"

The agent will:
1. Understand your query intent
2. Generate appropriate SQL SELECT queries
3. Execute queries safely (read-only)
4. Display results in a formatted, easy-to-read manner
5. Warn you if your query is not related to stock data

### Support Tickets

You can create support tickets in Trello:
1. Use the sidebar "Create Support Ticket" section
2. Enter a title and description
3. Click "Create Ticket"
4. The ticket will be created in your configured Trello board

## Safety Features

The application includes multiple safety layers:

1. **Query Validation**: Only SELECT queries are allowed
2. **Keyword Blocking**: Dangerous keywords (DELETE, DROP, TRUNCATE, etc.) are blocked
3. **Read-Only Mode**: UPDATE, INSERT, ALTER, and CREATE operations are prevented
4. **Result Limiting**: Queries are automatically limited to prevent excessive data retrieval
5. **Agent Instructions**: The AI agent is explicitly instructed to never perform dangerous operations
6. **Stock Query Detection**: Non-stock related queries are detected and users are warned

## Architecture

### Components

- **`app.py`**: Streamlit UI application
- **`agent.py`**: AI agent with Gemini AI integration
- **`support_ticket.py`**: Support ticket creation functionality (Trello)
- **`stock_database_setup.py`**: Stock database initialization script
- **`stock_data.db`**: SQLite database (created after running setup)

### Function Calling Tools

The agent uses three function calling tools:

1. **`execute_query`**: Executes SELECT queries on the database
2. **`get_table_schema`**: Retrieves table structure information
3. **`get_database_stats`**: Gets aggregated statistics about the database

## Database Schema

### stocks
- `id` (INTEGER, PRIMARY KEY)
- `stock_id` (INTEGER)
- `ticker` (TEXT) - Stock symbol (e.g., AAPL, MSFT)
- `company_name` (TEXT) - Full company name
- `sector` (TEXT) - Industry sector
- `price` (REAL) - Stock price
- `change` (REAL) - Price change
- `change_percent` (REAL) - Percentage change
- `volume` (INTEGER) - Trading volume
- `market_cap` (REAL) - Market capitalization
- `date` (DATE) - Date of the record

## Console Logging

All agent operations are logged to the console with timestamps:

```
2024-01-15 10:30:45 - __main__ - INFO - User message: Show me top stocks by volume
2024-01-15 10:30:46 - __main__ - INFO - Executing query: SELECT ...
2024-01-15 10:30:47 - __main__ - INFO - Query executed successfully. Returned 10 rows.
2024-01-15 10:30:48 - __main__ - INFO - Assistant response: Here are the top stocks...
```

## Troubleshooting

### Database not found
If you see "database not found" errors, run:
```bash
python stock_database_setup.py
```

### Gemini API errors
- Verify your API key is correct in `.env`
- Check your Google AI account has sufficient credits
- Ensure you have access to Gemini API
- The app uses `gemini-2.5-flash` model by default

### Support ticket creation fails
- Verify Trello credentials are set in `.env`
- Check API key and token are valid
- Ensure the board ID is correct
- Verify API tokens have appropriate permissions

### Model not found errors
If you see "model not found" errors, the app will automatically try:
1. `gemini-2.5-flash` (primary)
2. `gemini-pro-latest` (fallback)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
