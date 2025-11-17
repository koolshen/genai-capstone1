"""
AI Agent with function calling capabilities for stock data queries using Gemini AI.
Includes safety features to prevent dangerous operations.
"""
import os
import sqlite3
import logging
import json
from typing import List, Dict, Any, Tuple, Optional
import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Stock-related keywords for query validation
STOCK_KEYWORDS = [
    'stock', 'stocks', 'share', 'shares', 'ticker', 'symbol', 'price', 'volume',
    'market', 'trading', 'equity', 'equities', 'nasdaq', 'nyse', 'dow', 's&p',
    'portfolio', 'investment', 'investor', 'dividend', 'earnings', 'revenue',
    'company', 'companies', 'sector', 'industry', 'financial', 'finance'
]

class StockDataAgent:
    """AI Agent for querying stock data database using Gemini AI with safety features."""
    
    def __init__(self, db_path: str = 'stock_data.db'):
        self.db_path = db_path
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            # Use gemini-2.5-flash (available and fast) or fallback to gemini-pro-latest
            try:
                self.model = genai.GenerativeModel('gemini-2.5-flash')
            except Exception as e:
                logger.warning(f"Failed to initialize gemini-2.5-flash, trying gemini-pro-latest: {e}")
                self.model = genai.GenerativeModel('gemini-pro-latest')
        self.conversation_history = []
        
    def _is_stock_related_query(self, query: str) -> bool:
        """Check if the query is related to stock data."""
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in STOCK_KEYWORDS)
        
    def _check_safety(self, query: str) -> Tuple[bool, str]:
        """Check if query contains dangerous operations."""
        query_upper = query.upper().strip()
        
        # Block DELETE, DROP, TRUNCATE operations
        if any(keyword in query_upper for keyword in ['DELETE', 'DROP', 'TRUNCATE']):
            return False, "Dangerous operation detected: DELETE, DROP, or TRUNCATE operations are not allowed for safety."
        
        # Warn about ALTER, UPDATE, INSERT, CREATE operations
        if any(keyword in query_upper for keyword in ['ALTER', 'UPDATE', 'INSERT', 'CREATE TABLE', 'CREATE INDEX']):
            return False, "Modification operations (ALTER, UPDATE, INSERT, CREATE) are not allowed. This is a read-only database interface."
        
        return True, ""
    
    def execute_query(self, query: str, limit: int = 100) -> Dict[str, Any]:
        """
        Execute a SELECT query on the database.
        Only SELECT queries are allowed for safety.
        """
        logger.info(f"Executing query: {query}")
        
        # Safety check
        is_safe, error_msg = self._check_safety(query)
        if not is_safe:
            logger.warning(f"Unsafe query blocked: {query}")
            return {"error": error_msg, "data": None}
        
        # Ensure it's a SELECT query
        if not query.strip().upper().startswith('SELECT'):
            logger.warning(f"Non-SELECT query blocked: {query}")
            return {"error": "Only SELECT queries are allowed.", "data": None}
        
        try:
            if not os.path.exists(self.db_path):
                return {"error": f"Database file '{self.db_path}' not found.", "data": None}
                
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            cursor = conn.cursor()
            
            # Add LIMIT if not present and query might return many rows
            if 'LIMIT' not in query.upper():
                query = f"{query.rstrip(';')} LIMIT {limit}"
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Convert rows to list of dictionaries
            columns = [description[0] for description in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
            
            conn.close()
            
            logger.info(f"Query executed successfully. Returned {len(data)} rows.")
            return {"error": None, "data": data, "row_count": len(data)}
            
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            return {"error": str(e), "data": None}
    
    def get_table_schema(self, table_name: str = None) -> Dict[str, Any]:
        """Get schema information for tables."""
        logger.info(f"Getting schema for table: {table_name or 'all'}")
        
        try:
            if not os.path.exists(self.db_path):
                return {"error": f"Database file '{self.db_path}' not found."}
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if table_name:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                conn.close()
                return {"table": table_name, "columns": columns}
            else:
                # Get all tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                schemas = {}
                for table in tables:
                    cursor.execute(f"PRAGMA table_info({table})")
                    schemas[table] = cursor.fetchall()
                
                conn.close()
                return {"tables": schemas}
                
        except Exception as e:
            logger.error(f"Schema retrieval error: {str(e)}")
            return {"error": str(e)}
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get aggregated statistics about the stock database."""
        logger.info("Getting database statistics")
        
        try:
            if not os.path.exists(self.db_path):
                return {"error": f"Database file '{self.db_path}' not found."}
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            stats = {}
            
            # Count rows in each table
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[f"{table}_count"] = cursor.fetchone()[0]
            
            conn.close()
            logger.info("Database statistics retrieved successfully")
            return stats
            
        except Exception as e:
            logger.error(f"Statistics retrieval error: {str(e)}")
            return {"error": str(e)}
    
    def chat(self, user_message: str) -> Tuple[str, bool]:
        """
        Chat with the agent using Gemini AI to understand queries and execute database operations.
        Returns: (response_message, is_stock_related)
        """
        logger.info(f"User message: {user_message}")
        
        if not self.model:
            return ("Error: Gemini API key not configured. Please set GEMINI_API_KEY in your .env file.", True)
        
        # Check if query is stock-related
        is_stock_related = self._is_stock_related_query(user_message)
        
        if not is_stock_related:
            warning_msg = "Warning: This query doesn't appear to be related to stock data. This application is designed to answer questions about stock market data only. Please ask questions about stocks, companies, trading, or financial data."
            logger.warning(f"Non-stock query detected: {user_message}")
            return (warning_msg, False)
        
        if not os.path.exists(self.db_path):
            return (f"Error: Database file '{self.db_path}' not found. Please wait for stock data to be loaded.", True)
        
        # Get database schema first to help Gemini understand the structure
        schema_info = self.get_table_schema()
        schema_text = json.dumps(schema_info, indent=2, default=str)
        
        # System instruction with context
        system_instruction = f"""You are a helpful stock data assistant. You help users query a stock market database.

Database Schema:
{schema_text}

IMPORTANT RULES:
1. When a user asks a question, you should:
   - First understand what data they need
   - Generate a SQL SELECT query to get that data
   - Format your response as: SQL_QUERY: <the query here>
   - Then provide a natural language explanation

2. You can ONLY generate SELECT queries. Never generate DELETE, DROP, TRUNCATE, UPDATE, INSERT, ALTER, or CREATE operations.

3. When returning data, format it nicely with tables, insights, and summaries.

4. Focus on stock-related queries only.

Example:
User: "Show me top 10 stocks by volume"
You: "SQL_QUERY: SELECT * FROM stocks ORDER BY volume DESC LIMIT 10

Here are the top 10 stocks by trading volume: [then describe the results]"

Be helpful, concise, and safety-conscious."""
        
        try:
            # Build prompt with conversation history
            prompt_parts = [system_instruction]
            
            # Add recent conversation history
            for msg in self.conversation_history[-5:]:
                if msg.get("role") == "user":
                    prompt_parts.append(f"User: {msg.get('parts', [msg.get('content', '')])[0]}")
                elif msg.get("role") == "model":
                    content = msg.get('parts', [msg.get('content', '')])[0]
                    if isinstance(content, str):
                        prompt_parts.append(f"Assistant: {content}")
            
            prompt_parts.append(f"User: {user_message}")
            
            # Call Gemini API
            response = self.model.generate_content(
                prompt_parts,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 2048,
                }
            )
            
            assistant_message = response.text
            
            # Check if response contains SQL query
            if "SQL_QUERY:" in assistant_message:
                # Extract SQL query
                sql_part = assistant_message.split("SQL_QUERY:")[1].split("\n")[0].strip()
                if sql_part:
                    # Execute the query
                    query_result = self.execute_query(sql_part)
                    if query_result.get("error"):
                        assistant_message = f"{assistant_message}\n\nError executing query: {query_result['error']}"
                    else:
                        data = query_result.get("data", [])
                        row_count = query_result.get("row_count", 0)
                        if row_count > 0:
                            # Format data as table
                            df = pd.DataFrame(data)
                            data_table = df.to_string(index=False)
                            assistant_message = f"{assistant_message}\n\nQuery Results ({row_count} rows):\n```\n{data_table}\n```"
                        else:
                            assistant_message = f"{assistant_message}\n\nQuery returned 0 rows."
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "parts": [user_message]})
            self.conversation_history.append({"role": "model", "parts": [assistant_message]})
            
            logger.info(f"Assistant response: {assistant_message[:100]}...")
            return (assistant_message, True)
                
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return (f"I encountered an error: {str(e)}. Please try again or check your query.", True)
