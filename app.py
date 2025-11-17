"""
Streamlit application for Stock Data Insights App with Gemini AI Agent.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sqlite3
import os
import hashlib
from agent import StockDataAgent
from support_ticket import SupportTicketManager

# Page configuration
st.set_page_config(
    page_title="Stock Data Insights",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = StockDataAgent()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'ticket_manager' not in st.session_state:
    st.session_state.ticket_manager = SupportTicketManager()
if 'last_query_hash' not in st.session_state:
    st.session_state.last_query_hash = None
if 'query_processed' not in st.session_state:
    st.session_state.query_processed = False

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .warning-box {
        background-color: #1a1a2e;
        border: 2px solid #4a90e2;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #e0e0e0;
    }
    .stButton>button {
        width: 100%;
        background-color: #4a90e2;
        color: white;
    }
    .stButton>button:hover {
        background-color: #357abd;
    }
    /* Custom colors for alerts */
    div[data-testid="stAlert"] {
        border-radius: 0.5rem;
    }
    /* Warning messages - blue theme */
    div[data-testid="stAlert"] div[role="alert"] {
        background-color: #1a1a2e;
        border-left: 4px solid #4a90e2;
    }
    /* Error messages - red theme */
    div[data-baseweb="notification"] {
        background-color: #2d1b1b;
        border-left: 4px solid #e74c3c;
    }
    /* Info messages - green theme */
    div[data-testid="stAlert"]:has(svg[data-testid="stAlertIcon"]) {
        background-color: #1a2e1a;
        border-left: 4px solid #2ecc71;
    }
    </style>
""", unsafe_allow_html=True)

def get_database_stats():
    """Get database statistics for dashboard."""
    try:
        db_path = 'stock_data.db'
        if not os.path.exists(db_path):
            return None
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total records
        cursor.execute("SELECT COUNT(*) FROM stocks")
        stats['total_records'] = cursor.fetchone()[0]
        
        # Unique stocks
        cursor.execute("SELECT COUNT(DISTINCT ticker) FROM stocks")
        stats['unique_stocks'] = cursor.fetchone()[0]
        
        # Sectors
        cursor.execute("SELECT COUNT(DISTINCT sector) FROM stocks")
        stats['sectors'] = cursor.fetchone()[0]
        
        # Latest date data
        cursor.execute("SELECT MAX(date) FROM stocks")
        latest_date = cursor.fetchone()[0]
        stats['latest_date'] = latest_date
        
        # Top stocks by market cap (latest date)
        cursor.execute("""
            SELECT ticker, company_name, price, market_cap, volume, change_percent
            FROM stocks
            WHERE date = (SELECT MAX(date) FROM stocks)
            ORDER BY market_cap DESC
            LIMIT 10
        """)
        stats['top_by_market_cap'] = cursor.fetchall()
        
        # Stocks by sector
        cursor.execute("""
            SELECT sector, COUNT(DISTINCT ticker) as stock_count
            FROM stocks
            GROUP BY sector
            ORDER BY stock_count DESC
        """)
        stats['stocks_by_sector'] = cursor.fetchall()
        
        # Price statistics
        cursor.execute("""
            SELECT 
                AVG(price) as avg_price,
                MIN(price) as min_price,
                MAX(price) as max_price
            FROM stocks
            WHERE date = (SELECT MAX(date) FROM stocks)
        """)
        price_stats = cursor.fetchone()
        stats['avg_price'] = price_stats[0]
        stats['min_price'] = price_stats[1]
        stats['max_price'] = price_stats[2]
        
        # Top gainers (latest date)
        cursor.execute("""
            SELECT ticker, company_name, price, change, change_percent, volume
            FROM stocks
            WHERE date = (SELECT MAX(date) FROM stocks)
            ORDER BY change_percent DESC
            LIMIT 10
        """)
        stats['top_gainers'] = cursor.fetchall()
        
        # Top losers (latest date)
        cursor.execute("""
            SELECT ticker, company_name, price, change, change_percent, volume
            FROM stocks
            WHERE date = (SELECT MAX(date) FROM stocks)
            ORDER BY change_percent ASC
            LIMIT 10
        """)
        stats['top_losers'] = cursor.fetchall()
        
        # Highest volume (latest date)
        cursor.execute("""
            SELECT ticker, company_name, price, volume, change_percent
            FROM stocks
            WHERE date = (SELECT MAX(date) FROM stocks)
            ORDER BY volume DESC
            LIMIT 10
        """)
        stats['highest_volume'] = cursor.fetchall()
        
        conn.close()
        return stats
    except Exception as e:
        st.error(f"Error fetching stats: {str(e)}")
        return None

def create_support_ticket():
    """Create a support ticket dialog."""
    with st.sidebar:
        st.markdown("### Create Support Ticket")
        st.info("Tickets will be created in Trello")
        
        ticket_title = st.text_input("Ticket Title", key="ticket_title")
        ticket_description = st.text_area("Description", height=100, key="ticket_desc")
        
        if st.button("Create Ticket", key="create_ticket_btn"):
            if ticket_title and ticket_description:
                result = st.session_state.ticket_manager.create_ticket(
                    ticket_title,
                    ticket_description,
                    "trello"
                )
                
                if result.get("success"):
                    st.success("Ticket created successfully!")
                    st.info(f"Link: {result.get('url', 'N/A')}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"I've created a support ticket for you. You can view it here: {result.get('url', 'N/A')}"
                    })
                else:
                    st.error(f"Failed to create ticket: {result.get('error', 'Unknown error')}")
            else:
                st.warning("Please fill in both title and description.")

# Main app
st.markdown('<h1 class="main-header">Stock Data Insights App</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Quick Actions")
    
    if st.button("Refresh Dashboard"):
        st.rerun()
    
    st.markdown("---")
    
    # Support ticket section
    create_support_ticket()
    
    st.markdown("---")
    st.markdown("### Sample Stock Queries")
    st.markdown("""
    - Show me the top 10 stocks by market cap
    - What are the best performing stocks today?
    - Show me stocks from the technology sector
    - What is the average price of stocks in the S&P 500?
    - Show me stocks with highest trading volume
    """)

# Main content area
tab1, tab2 = st.tabs(["Dashboard", "Chat with Agent"])

with tab1:
    st.markdown("### Stock Data Overview")
    
    stats = get_database_stats()
    
    if not stats:
        st.info("Waiting for stock data to be loaded. Please run `python stock_database_setup.py` to create the database.")
        if st.button("Create Database Now"):
            import subprocess
            with st.spinner("Creating stock database..."):
                result = subprocess.run(["python", "stock_database_setup.py"], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("Database created successfully! Please refresh the page.")
                    st.rerun()
                else:
                    st.error(f"Error creating database: {result.stderr}")
    else:
        # Key metrics
        st.markdown("#### Market Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", f"{stats['total_records']:,}")
        
        with col2:
            st.metric("Unique Stocks", f"{stats['unique_stocks']:,}")
        
        with col3:
            st.metric("Sectors", f"{stats['sectors']}")
        
        with col4:
            st.metric("Latest Date", stats['latest_date'])
        
        st.markdown("---")
        
        # Price statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Price", f"${stats['avg_price']:.2f}")
        with col2:
            st.metric("Min Price", f"${stats['min_price']:.2f}")
        with col3:
            st.metric("Max Price", f"${stats['max_price']:.2f}")
        
        st.markdown("---")
        
        # Charts and tables
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Stocks by Sector")
            if stats['stocks_by_sector']:
                sector_df = pd.DataFrame(stats['stocks_by_sector'], columns=['Sector', 'Stock Count'])
                fig_pie = px.pie(sector_df, values='Stock Count', names='Sector', 
                               title="Distribution of Stocks by Sector")
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("#### Top 10 by Market Cap")
            if stats['top_by_market_cap']:
                market_cap_df = pd.DataFrame(stats['top_by_market_cap'], 
                                            columns=['Ticker', 'Company', 'Price', 'Market Cap', 'Volume', 'Change %'])
                market_cap_df['Market Cap'] = market_cap_df['Market Cap'].apply(lambda x: f"${x/1e9:.2f}B")
                market_cap_df['Price'] = market_cap_df['Price'].apply(lambda x: f"${x:.2f}")
                market_cap_df['Volume'] = market_cap_df['Volume'].apply(lambda x: f"{x:,}")
                market_cap_df['Change %'] = market_cap_df['Change %'].apply(lambda x: f"{x:.2f}%")
                st.dataframe(market_cap_df[['Ticker', 'Company', 'Price', 'Market Cap', 'Change %']], 
                           use_container_width=True, hide_index=True)
        
        # Top gainers and losers
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top Gainers")
            if stats['top_gainers']:
                gainers_df = pd.DataFrame(stats['top_gainers'], 
                                        columns=['Ticker', 'Company', 'Price', 'Change', 'Change %', 'Volume'])
                gainers_df['Price'] = gainers_df['Price'].apply(lambda x: f"${x:.2f}")
                gainers_df['Change'] = gainers_df['Change'].apply(lambda x: f"${x:+.2f}")
                gainers_df['Change %'] = gainers_df['Change %'].apply(lambda x: f"{x:+.2f}%")
                st.dataframe(gainers_df[['Ticker', 'Company', 'Price', 'Change', 'Change %']], 
                           use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### Top Losers")
            if stats['top_losers']:
                losers_df = pd.DataFrame(stats['top_losers'], 
                                       columns=['Ticker', 'Company', 'Price', 'Change', 'Change %', 'Volume'])
                losers_df['Price'] = losers_df['Price'].apply(lambda x: f"${x:.2f}")
                losers_df['Change'] = losers_df['Change'].apply(lambda x: f"${x:+.2f}")
                losers_df['Change %'] = losers_df['Change %'].apply(lambda x: f"{x:+.2f}%")
                st.dataframe(losers_df[['Ticker', 'Company', 'Price', 'Change', 'Change %']], 
                           use_container_width=True, hide_index=True)
        
        # Highest volume
        st.markdown("#### Highest Trading Volume")
        if stats['highest_volume']:
            volume_df = pd.DataFrame(stats['highest_volume'], 
                                   columns=['Ticker', 'Company', 'Price', 'Volume', 'Change %'])
            volume_df['Price'] = volume_df['Price'].apply(lambda x: f"${x:.2f}")
            volume_df['Volume'] = volume_df['Volume'].apply(lambda x: f"{x:,}")
            volume_df['Change %'] = volume_df['Change %'].apply(lambda x: f"{x:+.2f}%")
            st.dataframe(volume_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.info("Use the Chat tab to ask specific questions about the stock data. The AI will understand your queries and display relevant information.")

with tab2:
    # This tab shows chat messages - input is at bottom of page
    st.markdown("### Chat with Stock Data AI Agent")
    st.markdown("**Ask questions about stock data using natural language.** The AI will understand your intent and display relevant stock information.")
    
    # Warning banner
    st.markdown("""
    <div class="warning-box">
        <strong>Important:</strong> This application is designed to answer questions about <strong>stock market data only</strong>. 
        Please ask questions related to stocks, companies, trading, prices, volumes, or financial data.
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # Check if this is a warning message
            if message["content"].startswith("Warning:") or message["content"].startswith("WARNING:"):
                st.warning(message["content"])
            else:
                st.markdown(message["content"])
    
    # Chat input inside the tab
    st.markdown("---")
    
    # Use form for input clearing
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_query = st.text_input(
                "Ask a question about stock data",
                placeholder="e.g., 'Show me top stocks by volume'",
                label_visibility="collapsed"
            )
        with col2:
            submitted = st.form_submit_button("Send", type="primary", use_container_width=True)
    
    # Process query ONLY if form was just submitted with a non-empty query
    # AND we haven't processed this exact query before
    if submitted and user_query and user_query.strip():
        query_hash = hashlib.md5(user_query.strip().encode()).hexdigest()
        
        # Only process if this is a NEW query (different hash from last processed)
        if query_hash != st.session_state.last_query_hash:
            # IMMEDIATELY update hash BEFORE processing to prevent reprocessing
            st.session_state.last_query_hash = query_hash
            
            # Add user message to session state
            st.session_state.messages.append({"role": "user", "content": user_query.strip()})
            
            # Get agent response
            try:
                response, is_stock_related = st.session_state.agent.chat(user_query.strip())
                
                # Add assistant response to session state
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Show warning if not stock-related
                if not is_stock_related:
                    st.error("This query is not related to stock data. Please ask questions about stocks, companies, trading, or financial markets.")
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")
            
            # Rerun to show new messages (form will clear input automatically)
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Stock Data Insights App | Powered by Google Gemini AI | Built with Streamlit</p>
        <p>Safety Features: Read-only database access | Stock data queries only</p>
    </div>
    """,
    unsafe_allow_html=True
)
