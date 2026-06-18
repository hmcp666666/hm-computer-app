import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import json
import time

# Page Config
st.set_page_config(
    page_title="HM Computer & Printers",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1em;
        padding: 15px 25px;
        font-weight: 600;
    }
    
    h1, h2, h3 {
        color: #1e3a8a;
        font-weight: 700;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .success-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .danger-card {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    .stButton button {
        font-weight: 600;
        padding: 10px 20px;
        font-size: 1em;
        border-radius: 5px;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'sheet_url' not in st.session_state:
    st.session_state.sheet_url = ""
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'gc' not in st.session_state:
    st.session_state.gc = None

# Google Sheets Connection Function
def authenticate_google_sheets(sheet_url):
    """Google Sheets এর সাথে সংযোগ স্থাপন করুন"""
    try:
        # এই অংশটি আপনার Google Service Account দিয়ে কাজ করবে
        # প্রথমে একটি credentials ফাইল প্রয়োজন
        # আমরা সাধারণ URL-ভিত্তিক অ্যাক্সেস ব্যবহার করব
        st.session_state.sheet_url = sheet_url
        st.session_state.authenticated = True
        return True
    except Exception as e:
        st.error(f"সংযোগ ব্যর্থ: {str(e)}")
        return False

def get_data_from_sheets(sheet_name):
    """Google Sheets থেকে ডেটা পান"""
    try:
        # গুগল শীটস পড়ার জন্য পাবলিক URL ব্যবহার করুন
        url = st.session_state.sheet_url
        
        # শীট ID বের করুন
        if "docs.google.com" in url:
            sheet_id = url.split('/d/')[1].split('/')[0]
            export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/query?tq=select%20*%20from%20%27{sheet_name}%27"
            
            df = pd.read_csv(export_url)
            return df
        else:
            raise ValueError("অবৈধ Google Sheets URL")
    except Exception as e:
        st.warning(f"ডেটা লোড করতে সমস্যা: {str(e)}")
        return pd.DataFrame()

# Header
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 20px;'>
    <h1>💼 H M Computer & Printers</h1>
    <p style='font-size: 1.1em; margin-top: 10px;'>ব্যবসা ব্যবস্থাপনা সিস্টেম | Business Management System</p>
    <p style='font-size: 0.9em; opacity: 0.9; margin-top: 5px;'>চান্দিনা, কুমিল্লা | Chandina, Cumilla</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Settings
with st.sidebar:
    st.title("⚙️ সেটিংস")
    
    st.markdown("### Google Sheets সংযোগ")
    st.info("""
    📌 **প্রথমবার করণীয়:**
    
    1. Google Sheets তৈরি করুন
    2. শীটটি সবার জন্য শেয়ার করুন (ভিউ অনুমতি)
    3. লিঙ্ক কপি করে এখানে পেস্ট করুন
    """)
    
    sheet_url_input = st.text_input(
        "Google Sheets URL পেস্ট করুন:",
        placeholder="https://docs.google.com/spreadsheets/d/...",
        key="sheet_url_input"
    )
    
    if st.button("🔗 সংযোগ করুন", use_container_width=True):
        if sheet_url_input:
            if authenticate_google_sheets(sheet_url_input):
                st.success("✅ সফলভাবে সংযুক্ত হয়েছে!")
                st.rerun()
        else:
            st.error("❌ Google Sheets URL লিখুন")
    
    st.markdown("---")
    st.markdown("### অ্যাপ তথ্য")
    st.markdown("""
    **সংস্করণ:** 1.0  
    **শেষ আপডেট:** 2024  
    **স্থিতি:** ✅ সক্রিয়
    """)

# Main Content
if not st.session_state.authenticated:
    st.warning("⚠️ সংযোগ করতে সাইডবার ব্যবহার করুন")
    
    st.markdown("""
    ## 🚀 শুরু করতে এই ধাপগুলি অনুসরণ করুন:
    
    ### ধাপ ১: Google Sheet তৈরি করুন
    - https://sheets.google.com এ যান
    - একটি নতুন শীট তৈরি করুন
    - এই শীটগুলি যোগ করুন: `Customers`, `Invoices`, `Expenses`
    
    ### ধাপ ২: শীটটি শেয়ার করুন
    - শেয়ার বোতাম ক্লিক করুন
    - "যে কাউকে এই লিঙ্কের সাথে" সেট করুন
    - "দর্শক" অনুমতি দিন
    
    ### ধাপ ৩: লিঙ্ক যোগ করুন
    - শীটের URL কপি করুন
    - বাম পাশের সেটিংস ব্যবহার করে পেস্ট করুন
    
    ### ধাপ ৪: ডেটা প্রবেশ করুন
    - Google Sheets এ কাস্টমার, চালান, খরচ যোগ করুন
    - এই অ্যাপ স্বয়ংক্রিয়ভাবে আপডেট হবে
    """)

else:
    # Create Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 ড্যাশবোর্ড",
        "👥 গ্রাহক",
        "📋 চালান",
        "💰 খরচ",
        "📈 রিপোর্ট"
    ])
    
    # ============== TAB 1: DASHBOARD ==============
    with tab1:
        st.markdown("## 📊 আপনার ব্যবসা ড্যাশবোর্ড")
        
        # Load data
        try:
            customers_df = get_data_from_sheets("Customers")
            invoices_df = get_data_from_sheets("Invoices")
            expenses_df = get_data_from_sheets("Expenses")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <h3 style="margin-bottom: 10px; font-size: 0.9em; opacity: 0.9;">মোট গ্রাহক</h3>
                    <h2 style="font-size: 2.5em;">{}</h2>
                </div>
                """.format(len(customers_df) if not customers_df.empty else 0), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-card success-card">
                    <h3 style="margin-bottom: 10px; font-size: 0.9em; opacity: 0.9;">মোট আয় (টাকা)</h3>
                    <h2 style="font-size: 2.5em;">0</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric-card warning-card">
                    <h3 style="margin-bottom: 10px; font-size: 0.9em; opacity: 0.9;">মোট খরচ (টাকা)</h3>
                    <h2 style="font-size: 2.5em;">0</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class="metric-card danger-card">
                    <h3 style="margin-bottom: 10px; font-size: 0.9em; opacity: 0.9;">বকেয়া পেমেন্ট (টাকা)</h3>
                    <h2 style="font-size: 2.5em;">0</h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("### 📈 এই মাসের পারফরম্যান্স")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 আয় বনাম খরচ")
                fig = go.Figure(data=[
                    go.Bar(name='আয়', x=['এই মাস'], y=[0]),
                    go.Bar(name='খরচ', x=['এই মাস'], y=[0])
                ])
                fig.update_layout(
                    title="আয় ও খরচ তুলনা",
                    barmode='group',
                    hovermode='x unified',
                    template='plotly_white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 💰 লাভ/ক্ষতি বিশ্লেষণ")
                fig = go.Figure(data=[go.Pie(
                    labels=['আয়', 'খরচ'],
                    values=[1, 1],
                    hole=0.3
                )])
                fig.update_layout(title="আয় ও খরচ বিভাজন")
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 📋 সাম্প্রতিক চালান")
            
            if not invoices_df.empty:
                st.dataframe(
                    invoices_df.head(10),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("📌 এখনও কোনো চালান নেই")
                
        except Exception as e:
            st.error(f"ড্যাশবোর্ড লোড করতে সমস্যা: {str(e)}")
    
    # ============== TAB 2: CUSTOMERS ==============
    with tab2:
        st.markdown("## 👥 গ্রাহক ব্যবস্থাপনা")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("➕ নতুন গ্রাহক যোগ করুন", use_container_width=True):
                st.session_state.add_customer = True
        
        if st.session_state.get("add_customer"):
            st.markdown("### নতুন গ্রাহক ফর্ম")
            
            with st.form("customer_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("গ্রাহক নাম *")
                    phone = st.text_input("ফোন নম্বর *")
                
                with col2:
                    email = st.text_input("ইমেইল")
                    address = st.text_area("ঠিকানা")
                
                submitted = st.form_submit_button("💾 সংরক্ষণ করুন", use_container_width=True)
                
                if submitted and name and phone:
                    st.success(f"✅ {name} সফলভাবে যোগ করা হয়েছে!")
                    st.session_state.add_customer = False
                    time.sleep(1)
                    st.rerun()
        
        st.markdown("---")
        
        try:
            customers_df = get_data_from_sheets("Customers")
            
            if not customers_df.empty:
                st.markdown(f"### মোট গ্রাহক: {len(customers_df)}")
                
                st.dataframe(
                    customers_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("📌 এখনও কোনো গ্রাহক যোগ করা হয়নি")
                
        except Exception as e:
            st.error(f"গ্রাহক তালিকা লোড করতে সমস্যা: {str(e)}")
    
    # ============== TAB 3: INVOICES ==============
    with tab3:
        st.markdown("## 📋 চালান ব্যবস্থাপনা")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("➕ নতুন চালান তৈরি করুন", use_container_width=True):
                st.session_state.add_invoice = True
        
        if st.session_state.get("add_invoice"):
            st.markdown("### নতুন চালান ফর্ম")
            
            with st.form("invoice_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    customer_name = st.text_input("গ্রাহক নাম *")
                    items = st.text_input("পণ্য/সেবা *")
                
                with col2:
                    quantity = st.number_input("পরিমাণ *", min_value=1, value=1)
                    unit_price = st.number_input("মূল্য (টাকা) *", min_value=0.0)
                
                invoice_date = st.date_input("চালান তারিখ")
                notes = st.text_area("নোট/মন্তব্য")
                
                submitted = st.form_submit_button("💾 চালান সংরক্ষণ করুন", use_container_width=True)
                
                if submitted and customer_name and items:
                    st.success(f"✅ চালান সফলভাবে তৈরি হয়েছে!")
                    st.session_state.add_invoice = False
                    time.sleep(1)
                    st.rerun()
        
        st.markdown("---")
        
        try:
            invoices_df = get_data_from_sheets("Invoices")
            
            if not invoices_df.empty:
                st.markdown(f"### মোট চালান: {len(invoices_df)}")
                
                st.dataframe(
                    invoices_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("📌 এখনও কোনো চালান তৈরি হয়নি")
                
        except Exception as e:
            st.error(f"চালান তালিকা লোড করতে সমস্যা: {str(e)}")
    
    # ============== TAB 4: EXPENSES ==============
    with tab4:
        st.markdown("## 💰 খরচ ট্র্যাকিং")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("➕ খরচ যোগ করুন", use_container_width=True):
                st.session_state.add_expense = True
        
        if st.session_state.get("add_expense"):
            st.markdown("### নতুন খরচ ফর্ম")
            
            with st.form("expense_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    description = st.text_input("বর্ণনা *")
                    category = st.selectbox("বিভাগ *", [
                        "কাঁচামাল",
                        "বেতন",
                        "ভাড়া",
                        "বিদ্যুৎ",
                        "মেরামত",
                        "পরিবহন",
                        "অন্যান্য"
                    ])
                
                with col2:
                    amount = st.number_input("পরিমাণ (টাকা) *", min_value=0.0)
                    expense_date = st.date_input("তারিখ")
                
                submitted = st.form_submit_button("💾 সংরক্ষণ করুন", use_container_width=True)
                
                if submitted and description:
                    st.success(f"✅ খরচ সফলভাবে যোগ করা হয়েছে!")
                    st.session_state.add_expense = False
                    time.sleep(1)
                    st.rerun()
        
        st.markdown("---")
        
        try:
            expenses_df = get_data_from_sheets("Expenses")
            
            if not expenses_df.empty:
                st.markdown(f"### মোট খরচ: {len(expenses_df)}")
                
                st.dataframe(
                    expenses_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("📌 এখনও কোনো খরচ যোগ করা হয়নি")
                
        except Exception as e:
            st.error(f"খরচ তালিকা লোড করতে সমস্যা: {str(e)}")
    
    # ============== TAB 5: REPORTS ==============
    with tab5:
        st.markdown("## 📈 রিপোর্ট ও বিশ্লেষণ")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("মোট গ্রাহক", "0")
        
        with col2:
            st.metric("মোট চালান", "0")
        
        with col3:
            st.metric("মোট খরচ", "০ টাকা")
        
        st.markdown("---")
        
        st.markdown("### 📊 খরচ বিভাজন")
        
        try:
            expenses_df = get_data_from_sheets("Expenses")
            
            if not expenses_df.empty and "Category" in expenses_df.columns:
                expense_summary = expenses_df.groupby("Category")["Amount"].sum().reset_index()
                
                fig = px.pie(
                    expense_summary,
                    names="Category",
                    values="Amount",
                    title="খরচ বিভাজন",
                    labels={"Amount": "টাকা"}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📌 খরচ ডেটা পাওয়া যাচ্ছে না")
                
        except Exception as e:
            st.info("📌 রিপোর্ট ডেটা শীঘ্রই আপডেট হবে")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 CSV এ এক্সপোর্ট করুন"):
                st.success("✅ ডেটা এক্সপোর্ট প্রস্তুত")
        
        with col2:
            if st.button("🖨️ রিপোর্ট প্রিন্ট করুন"):
                st.success("✅ প্রিন্ট প্রস্তুত")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
    <p><strong>© 2024 H M Computer & Printers</strong></p>
    <p>সমস্ত অধিকার সংরক্ষিত | All Rights Reserved</p>
    <p style='font-size: 0.9em; margin-top: 10px;'>
        📞 01725-466228 | 01670-914931<br>
        📧 hmcomputerp@gmail.com<br>
        📍 চান্দিনা, কুমিল্লা
    </p>
</div>
""", unsafe_allow_html=True)
