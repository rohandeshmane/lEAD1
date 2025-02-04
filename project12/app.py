import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import requests

# Configure page settings
st.set_page_config(
    page_title="AI Lead Management Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced futuristic CSS with advanced animations
st.markdown("""
<style>
    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(135deg, #2A0A5E 0%, #007BFF 100%);
        animation: gradientBG 15s ease infinite;
        background-size: 400% 400%;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Advanced Sidebar */
    .css-1d391kg {
        background: rgba(13, 17, 23, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(32, 201, 151, 0.1);
    }
    
    /* Sidebar nav items with hover effects */
    .css-1d391kg .streamlit-expanderHeader {
        background: rgba(32, 201, 151, 0.05);
        border-radius: 8px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .css-1d391kg .streamlit-expanderHeader:hover {
        background: rgba(32, 201, 151, 0.1);
        transform: translateX(5px);
    }
    
    /* Headers with gradient text */
    h1 {
        background: linear-gradient(90deg, #20C997, #0ABDE3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        margin-bottom: 2rem !important;
    }
    
    h2, h3 {
        color: #20C997 !important;
        font-weight: 600 !important;
        text-shadow: 0 0 20px rgba(32, 201, 151, 0.3);
    }
    
    /* Advanced Cards with glassmorphism */
    .card {
        background: rgba(13, 17, 23, 0.8);
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        border: 1px solid rgba(32, 201, 151, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(32, 201, 151, 0.15);
    }
    
    /* Futuristic Metrics */
    .css-1xarl3l {
        background: rgba(13, 17, 23, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        border: 1px solid rgba(32, 201, 151, 0.1) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .css-1xarl3l:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(32, 201, 151, 0.15) !important;
    }
    
    /* Advanced Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0ABDE3, #20C997) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 20px rgba(10, 189, 227, 0.3) !important;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    /* Advanced Inputs */
    .stTextInput>div>div>input {
        background: rgba(13, 17, 23, 0.8) !important;
        border: 1px solid rgba(32, 201, 151, 0.3) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #20C997 !important;
        box-shadow: 0 0 0 2px rgba(32, 201, 151, 0.2) !important;
        transform: translateY(-2px);
    }
    
    /* Advanced Select boxes */
    .stSelectbox>div>div>select {
        background: rgba(13, 17, 23, 0.8) !important;
        border: 1px solid rgba(32, 201, 151, 0.3) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox>div>div>select:focus {
        border-color: #20C997 !important;
        box-shadow: 0 0 0 2px rgba(32, 201, 151, 0.2) !important;
        transform: translateY(-2px);
    }
    
    /* Advanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        padding: 0.5rem;
        border-radius: 16px;
        background: rgba(13, 17, 23, 0.5);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(13, 17, 23, 0.8);
        border-radius: 12px;
        padding: 1rem 2rem;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #0ABDE3, #20C997) !important;
        font-weight: 500;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(13, 17, 23, 0.8) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(32, 201, 151, 0.1) !important;
    }
    
    .dataframe th {
        background: rgba(32, 201, 151, 0.1) !important;
        color: #20C997 !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(13, 17, 23, 0.8);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #0ABDE3, #20C997);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #20C997, #0ABDE3);
    }
    
    /* Navigation Menu Animation */
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .nav-item {
        animation: slideIn 0.5s ease forwards;
        opacity: 0;
        animation-delay: calc(var(--item-number) * 0.1s);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Sidebar with animated navigation
st.sidebar.markdown("""
    <div style='padding: 1rem 0; text-align: center;'>
        <h1 style='font-size: 1.5rem; margin: 0;'>🤖 AI Lead Manager</h1>
        <div style='width: 50%; height: 2px; background: linear-gradient(90deg, #0ABDE3, #20C997); margin: 1rem auto;'></div>
    </div>
""", unsafe_allow_html=True)

# Navigation items with animation delays
nav_items = {
    "📊 Dashboard": 0,
    "👥 Leads": 1,
    "💬 Communications": 2,
    "⚙️ AI Settings": 3,
    "📈 Analytics": 4
}

# Create animated navigation items
for item, delay in nav_items.items():
    st.sidebar.markdown(f"""
        <div class='nav-item' style='--item-number: {delay};'>
            <div style='padding: 0.75rem 1rem; margin: 0.5rem 0; border-radius: 12px; 
                      background: rgba(32, 201, 151, 0.05); cursor: pointer; 
                      transition: all 0.3s ease;'
                 onmouseover="this.style.background='rgba(32, 201, 151, 0.1)'; this.style.transform='translateX(5px)'"
                 onmouseout="this.style.background='rgba(32, 201, 151, 0.05)'; this.style.transform='translateX(0px)'">
                {item}
            </div>
        </div>
    """, unsafe_allow_html=True)

# Add WhatsApp Lead Handling to Communications Tab
def handle_whatsapp_section():
    st.markdown("### 📱 WhatsApp Lead Management")
    
    # WhatsApp Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active WhatsApp Leads", "23", "↑ 5")
    with col2:
        st.metric("Pending Calls", "7", "↓ 2")
    with col3:
        st.metric("Call Acceptance Rate", "78%", "↑ 8%")
    
    # WhatsApp Lead Queue
    st.markdown("#### Incoming WhatsApp Leads")
    whatsapp_leads = [
        {"phone": "+1234567890", "status": "Pending Call", "time": "2 min ago"},
        {"phone": "+0987654321", "status": "Call Scheduled", "time": "5 min ago"},
        {"phone": "+1122334455", "status": "Call Completed", "time": "15 min ago"}
    ]
    
    for lead in whatsapp_leads:
        with st.container():
            cols = st.columns([2, 2, 2, 1])
            with cols[0]:
                st.write(f"📱 {lead['phone']}")
            with cols[1]:
                st.write(lead['status'])
            with cols[2]:
                st.write(lead['time'])
            with cols[3]:
                if lead['status'] == "Pending Call":
                    st.button("📞 Call Now", key=f"call_{lead['phone']}")

    # Call Analytics
    st.markdown("#### AI Call Analytics")
    call_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-03-01', end='2024-03-14'),
        'Calls': np.random.randint(10, 30, size=14),
        'Acceptance': np.random.uniform(0.6, 0.9, size=14)
    })
    
    tab1, tab2 = st.tabs(["📊 Call Volume", "📈 Acceptance Rate"])
    with tab1:
        st.line_chart(call_data.set_index('Date')['Calls'])
    with tab2:
        st.line_chart(call_data.set_index('Date')['Acceptance'])

    # Settings for AI Calls
    with st.expander("🎙️ AI Call Settings"):
        st.selectbox("Voice Selection", ["Bella", "Antoni", "Rachel", "James"])
        st.slider("Speech Rate", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        st.text_area("Custom Introduction", 
            "Hello! I'm your AI assistant. I'd love to learn more about your needs. How may I help you today?")
        st.button("Save Call Settings")

def show_communications():
    st.title("Communications Hub")
    
    # Main Communication Channels
    tabs = st.tabs(["📱 WhatsApp", "📧 Email", "💬 Chat", "📞 Calls", "📝 Notes"])
    
    with tabs[0]:  # WhatsApp Tab
        handle_whatsapp_section()
    
    with tabs[1]:  # Email Tab
        st.subheader("Email Communications")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.text_area("Compose Email", height=200)
            st.button("Send Email")
        with col2:
            st.markdown("### Templates")
            st.selectbox("Select Template", ["Welcome Message", "Follow-up", "Meeting Request"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[2]:  # Chat Tab
        st.subheader("Chat Communications")
        # Add chat functionality here
        pass
    
    with tabs[3]:  # Calls Tab
        st.subheader("Call Management")
        # Add calls functionality here
        pass
    
    with tabs[4]:  # Notes Tab
        st.subheader("Notes & Documentation")
        # Add notes functionality here
        pass

def show_dashboard():
    st.title("AI Lead Management Dashboard")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", "1,234", "+12%")
    with col2:
        st.metric("Response Rate", "95%", "+5%")
    with col3:
        st.metric("AI Accuracy", "89%", "+3%")
    with col4:
        st.metric("Conversion Rate", "23%", "+7%")
    
    # Charts Row
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        dates, response_times, _ = generate_sample_data()
        fig = px.line(
            x=dates, y=response_times,
            title="Average Response Time (minutes)",
            labels={"x": "Date", "y": "Minutes"}
        )
        fig.update_layout(
            plot_bgcolor='rgba(13, 17, 23, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        _, _, conversion_rates = generate_sample_data()
        fig = px.bar(
            x=dates, y=conversion_rates,
            title="Lead Conversion Rate",
            labels={"x": "Date", "y": "Rate"}
        )
        fig.update_layout(
            plot_bgcolor='rgba(13, 17, 23, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_leads():
    st.title("Lead Management")
    
    # Search and Filter Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox("Status", ["All", "New", "Qualified", "Converted", "Lost"])
    with col2:
        st.selectbox("Source", ["All", "Website", "Email", "WhatsApp", "Phone"])
    with col3:
        st.text_input("🔍 Search Leads", placeholder="Search by name, email...")
    
    # Lead Table
    st.markdown('<div class="card">', unsafe_allow_html=True)
    leads_data = pd.DataFrame({
        "Name": ["John Doe", "Jane Smith", "Mike Johnson"],
        "Email": ["john@example.com", "jane@example.com", "mike@example.com"],
        "Status": ["New", "Qualified", "Converted"],
        "Source": ["Website", "Email", "WhatsApp"],
        "Last Contact": ["2024-03-14", "2024-03-13", "2024-03-12"]
    })
    st.dataframe(leads_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_settings():
    st.title("AI Configuration")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Knowledge Base")
    st.file_uploader("Upload Training Data", accept_multiple_files=True)
    
    st.subheader("Response Templates")
    template_text = st.text_area("Default Response Template")
    
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("AI Confidence Threshold", 0.0, 1.0, 0.8)
    with col2:
        st.selectbox("Handoff Trigger", ["Low Confidence", "Keywords", "Sentiment", "Custom Rule"])
    
    st.button("Save Settings")
    st.markdown('</div>', unsafe_allow_html=True)

def show_analytics():
    st.title("Analytics & Reporting")
    
    # Date Range Selector
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        st.date_input("End Date", datetime.now())
    
    # Metrics Cards
    st.markdown('<div class="card">', unsafe_allow_html=True)
    metrics_cols = st.columns(4)
    with metrics_cols[0]:
        st.metric("Total Conversations", "2,456", "+15%")
    with metrics_cols[1]:
        st.metric("Avg. Response Time", "2.3 min", "-18%")
    with metrics_cols[2]:
        st.metric("AI Resolution Rate", "78%", "+5%")
    with metrics_cols[3]:
        st.metric("Customer Satisfaction", "4.6/5", "+0.3")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Performance Charts
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = go.Figure(data=[
            go.Pie(labels=['Email', 'WhatsApp', 'Voice'], 
                  values=[45, 35, 20],
                  hole=.3)
        ])
        fig.update_layout(
            title="Channel Distribution",
            plot_bgcolor='rgba(13, 17, 23, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = go.Figure(data=[
            go.Bar(name='AI Handled', x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], y=[20, 25, 30, 22, 28]),
            go.Bar(name='Human Handled', x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], y=[10, 8, 12, 9, 11])
        ])
        fig.update_layout(
            barmode='stack',
            title="Weekly Conversation Distribution",
            plot_bgcolor='rgba(13, 17, 23, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Generate sample data for demonstration
def generate_sample_data():
    dates = pd.date_range(start='2024-01-01', end='2024-03-14', freq='D')
    response_times = [3 + abs(np.sin(i/10)) for i in range(len(dates))]
    conversion_rates = [0.2 + 0.1 * abs(np.sin(i/15)) for i in range(len(dates))]
    return dates, response_times, conversion_rates

# Update the main navigation to include the enhanced communications section
nav_options = {
    "📊 Dashboard": show_dashboard,
    "👥 Leads": show_leads,
    "💬 Communications": show_communications,
    "⚙️ AI Settings": show_settings,
    "📈 Analytics": show_analytics
}

# Create radio buttons for navigation
selected = st.sidebar.radio(
    "Navigation",
    list(nav_options.keys()),
    label_visibility="collapsed"
)

# Show the selected page
nav_options[selected]()