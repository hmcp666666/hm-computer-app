import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Page Configuration
st.set_page_config(
    page_title="HM Computer & Printers",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    h1, h2, h3 {
        color: #1e3a8a;
    }
    
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-weight: bold;
    }
    
    .metric-purple {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-green {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .metric-yellow {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .metric-red {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'customers' not in st.session_state:
    st.session_state.customers = []
if 'invoices' not in st.session_state:
    st.session_state.invoices = []
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = True

# Header
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 20px;'>
    <h1>💼 H M Computer & Printers</h1>
    <p style='font-size: 1.1em; margin-top: 10px;'>ব্যবসা ব্যবস্থাপনা সিস্টেম</p>
    <p style='font-size: 0.9em; opacity: 0.9;'>পেশাদার ব্যবসায়িক সমাধান | Professional Business Solution</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ সেটিংস")
    
    st.markdown("### 📌 মোড নির্বাচন করুন")
    mode = st.radio(
        "কোন মোডে কাজ করতে চান?",
        ["📱 ডেমো মোড", "📊 Google Sheets সংযোগ"]
    )
    
    if mode == "📱 ডেমো মোড":
        st.session_state.demo_mode = True
        st.success("✅ ডেমো মোড সক্রিয়")
        st.info("""
        ডেমো মোডে:
        - নমুনা ডেটা দিয়ে কাজ করুন
        - সব ফিচার পরীক্ষা করুন
        - আপনার Google Sheets সংযুক্ত করতে প্রস্তুত হন
        """)
    else:
        st.session_state.demo_mode = False
        st.markdown("### 🔗 Google Sheets সংযোগ")
        
        st.info("""
        #### পদক্ষেপ:
        1. Google Sheets তৈরি করুন
        2. শীটটি শেয়ার করুন (সবার জন্য দর্শনযোগ্য)
        3. URL নীচে পেস্ট করুন
        """)
        
        sheet_url = st.text_input(
            "Google Sheets URL:",
            placeholder="https://docs.google.com/spreadsheets/d/..."
        )
        
        if sheet_url:
            st.success("✅ URL প্রাপ্ত। (পরবর্তী সংস্করণে সক্রিয় হবে)")
    
    st.markdown("---")
    st.markdown("### 📞 যোগাযোগ")
    st.markdown("""
    📱 01725-466228  
    📱 01670-914931  
    📧 hmcomputerp@gmail.com
    """)

# Main Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 ড্যাশবোর্ড",
    "👥 গ্রাহক",
    "📋 চালান",
    "💰 খরচ",
    "📈 রিপোর্ট"
])

# ============== DASHBOARD ==============
with tab1:
    st.markdown("## 📊 ব্যবসা ড্যাশবোর্ড")
    
    # Demo Data
    if st.session_state.demo_mode:
        # Calculate metrics
        total_customers = len(st.session_state.customers) if st.session_state.customers else 5
        total_income = sum([inv.get('total', 0) for inv in st.session_state.invoices]) if st.session_state.invoices else 15000
        total_expenses = sum([exp.get('amount', 0) for exp in st.session_state.expenses]) if st.session_state.expenses else 5000
        pending_amount = 10000
        
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card metric-purple">
                <div style="font-size: 0.9em; opacity: 0.9;">মোট গ্রাহক</div>
                <div style="font-size: 2.5em; margin-top: 10px;">{total_customers}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card metric-green">
                <div style="font-size: 0.9em; opacity: 0.9;">মোট আয়</div>
                <div style="font-size: 2.5em; margin-top: 10px;">৳{total_income:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card metric-yellow">
                <div style="font-size: 0.9em; opacity: 0.9;">মোট খরচ</div>
                <div style="font-size: 2.5em; margin-top: 10px;">৳{total_expenses:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            profit = total_income - total_expenses
            st.markdown(f"""
            <div class="metric-card metric-red">
                <div style="font-size: 0.9em; opacity: 0.9;">বকেয়া</div>
                <div style="font-size: 2.5em; margin-top: 10px;">৳{pending_amount:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 আয় ও খরচ")
            chart_data = pd.DataFrame({
                'ক্যাটাগরি': ['আয়', 'খরচ'],
                'পরিমাণ': [total_income, total_expenses]
            })
            st.bar_chart(chart_data.set_index('ক্যাটাগরি'))
        
        with col2:
            st.markdown("#### 💰 লাভ বিশ্লেষণ")
            profit = total_income - total_expenses
            st.markdown(f"""
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px; text-align: center;">
                <p style="font-size: 0.9em; color: #666;">নেট লাভ/ক্ষতি</p>
                <h2 style="color: {'#10b981' if profit > 0 else '#ef4444'}; margin: 10px 0;">৳{profit:,}</h2>
                <p style="font-size: 0.85em; color: #999;">({((profit/total_income)*100):.1f}% মার্জিন)</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📋 সাম্প্রতিক কার্যক্রম")
        
        # Sample data
        sample_data = {
            'চালান নম্বর': ['INV-001', 'INV-002', 'INV-003'],
            'গ্রাহক': ['রহিম দোকান', 'আলী স্টোর', 'ফারিহা অফিস'],
            'পরিমাণ (টাকা)': [5000, 8000, 2000],
            'অবস্থা': ['প্রদত্ত', 'অপেক্ষারত', 'প্রদত্ত'],
            'তারিখ': ['2024-01-15', '2024-01-16', '2024-01-17']
        }
        
        df_sample = pd.DataFrame(sample_data)
        st.dataframe(df_sample, use_container_width=True, hide_index=True)

# ============== CUSTOMERS ==============
with tab2:
    st.markdown("## 👥 গ্রাহক ব্যবস্থাপনা")
    
    col1, col2 = st.columns([4, 1])
    
    with col2:
        if st.button("➕ যোগ করুন", use_container_width=True):
            st.session_state.show_customer_form = True
    
    if st.session_state.get("show_customer_form", False):
        st.markdown("### নতুন গ্রাহক যোগ করুন")
        
        with st.form("customer_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("নাম *", placeholder="গ্রাহকের নাম")
                phone = st.text_input("ফোন *", placeholder="01XXX-XXXXXX")
            
            with col2:
                email = st.text_input("ইমেইল", placeholder="example@gmail.com")
                address = st.text_area("ঠিকানা", placeholder="সম্পূর্ণ ঠিকানা")
            
            submitted = st.form_submit_button("💾 সংরক্ষণ করুন")
            
            if submitted and name and phone:
                st.session_state.customers.append({
                    'id': len(st.session_state.customers) + 1,
                    'name': name,
                    'phone': phone,
                    'email': email,
                    'address': address,
                    'date': datetime.now().strftime("%Y-%m-%d")
                })
                st.success(f"✅ {name} সফলভাবে যোগ করা হয়েছে!")
                st.session_state.show_customer_form = False
                st.rerun()
    
    st.markdown("---")
    
    if st.session_state.customers:
        st.markdown(f"### মোট গ্রাহক: {len(st.session_state.customers)}")
        df = pd.DataFrame(st.session_state.customers)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        if st.session_state.demo_mode:
            st.info("📌 ডেমো মোডে 5 জন নমুনা গ্রাহক রয়েছে")
            
            demo_customers = [
                {'নাম': 'রহিম দোকান', 'ফোন': '01712345678', 'ইমেইল': 'rahim@email.com', 'ঠিকানা': 'চান্দিনা বাজার'},
                {'নাম': 'আলী স্টোর', 'ফোন': '01823456789', 'ইমেইল': 'ali@email.com', 'ঠিকানা': 'শহর কেন্দ্র'},
                {'নাম': 'ফারিহা অফিস', 'ফোন': '01934567890', 'ইমেইল': 'fariha@email.com', 'ঠিকানা': 'অফিস এলাকা'},
            ]
            
            df_demo = pd.DataFrame(demo_customers)
            st.dataframe(df_demo, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ এখনও কোনো গ্রাহক নেই")

# ============== INVOICES ==============
with tab3:
    st.markdown("## 📋 চালান ব্যবস্থাপনা")
    
    col1, col2 = st.columns([4, 1])
    
    with col2:
        if st.button("➕ নতুন", use_container_width=True):
            st.session_state.show_invoice_form = True
    
    if st.session_state.get("show_invoice_form", False):
        st.markdown("### নতুন চালান তৈরি করুন")
        
        with st.form("invoice_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                customer_name = st.text_input("গ্রাহক নাম *")
                invoice_no = st.text_input("চালান নম্বর", value=f"INV-{len(st.session_state.invoices)+1}")
            
            with col2:
                items = st.text_input("পণ্য/সেবা *", placeholder="যেমন: প্রিন্টিং সেবা")
                quantity = st.number_input("পরিমাণ", min_value=1, value=1)
            
            unit_price = st.number_input("মূল্য (টাকা) *", min_value=0.0)
            invoice_date = st.date_input("তারিখ", value=datetime.now())
            status = st.selectbox("অবস্থা", ["অপেক্ষারত", "প্রদত্ত"])
            
            submitted = st.form_submit_button("💾 সংরক্ষণ করুন")
            
            if submitted and customer_name and items:
                st.session_state.invoices.append({
                    'invoice_number': invoice_no,
                    'customer': customer_name,
                    'items': items,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total': quantity * unit_price,
                    'status': status,
                    'date': invoice_date.strftime("%Y-%m-%d")
                })
                st.success("✅ চালান সফলভাবে তৈরি হয়েছে!")
                st.session_state.show_invoice_form = False
                st.rerun()
    
    st.markdown("---")
    
    if st.session_state.invoices:
        st.markdown(f"### মোট চালান: {len(st.session_state.invoices)}")
        df = pd.DataFrame(st.session_state.invoices)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        if st.session_state.demo_mode:
            st.info("📌 ডেমো চালান দেখছেন")
            
            demo_invoices = [
                {'চালান': 'INV-001', 'গ্রাহক': 'রহিম দোকান', 'পণ্য': 'ব্যানার প্রিন্টিং', 'পরিমাণ': 2, 'মূল্য': 5000, 'মোট': 10000, 'অবস্থা': 'প্রদত্ত'},
                {'চালান': 'INV-002', 'গ্রাহক': 'আলী স্টোর', 'পণ্য': 'ডিজিটাল প্রিন্ট', 'পরিমাণ': 1, 'মূল্য': 8000, 'মোট': 8000, 'অবস্থা': 'অপেক্ষারত'},
            ]
            
            df_demo = pd.DataFrame(demo_invoices)
            st.dataframe(df_demo, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ এখনও কোনো চালান নেই")

# ============== EXPENSES ==============
with tab4:
    st.markdown("## 💰 খরচ ট্র্যাকিং")
    
    col1, col2 = st.columns([4, 1])
    
    with col2:
        if st.button("➕ যোগ করুন", use_container_width=True):
            st.session_state.show_expense_form = True
    
    if st.session_state.get("show_expense_form", False):
        st.markdown("### নতুন খরচ রেকর্ড করুন")
        
        with st.form("expense_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                description = st.text_input("বর্ণনা *", placeholder="যেমন: কাগজ ক্রয়")
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
                expense_date = st.date_input("তারিখ", value=datetime.now())
            
            submitted = st.form_submit_button("💾 সংরক্ষণ করুন")
            
            if submitted and description:
                st.session_state.expenses.append({
                    'description': description,
                    'category': category,
                    'amount': amount,
                    'date': expense_date.strftime("%Y-%m-%d")
                })
                st.success("✅ খরচ সফলভাবে যোগ করা হয়েছে!")
                st.session_state.show_expense_form = False
                st.rerun()
    
    st.markdown("---")
    
    if st.session_state.expenses:
        st.markdown(f"### মোট খরচ রেকর্ড: {len(st.session_state.expenses)}")
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        if st.session_state.demo_mode:
            st.info("📌 ডেমো খরচ ডেটা দেখছেন")
            
            demo_expenses = [
                {'বিবরণ': 'কাগজ ও কার্টিজ ক্রয়', 'বিভাগ': 'কাঁচামাল', 'পরিমাণ': 3000, 'তারিখ': '2024-01-15'},
                {'বিবরণ': 'অফিস ভাড়া', 'বিভাগ': 'ভাড়া', 'পরিমাণ': 2000, 'তারিখ': '2024-01-01'},
                {'বিবরণ': 'বিদ্যুৎ বিল', 'বিভাগ': 'বিদ্যুৎ', 'পরিমাণ': 800, 'তারিখ': '2024-01-10'},
            ]
            
            df_demo = pd.DataFrame(demo_expenses)
            st.dataframe(df_demo, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ এখনও কোনো খরচ নেই")

# ============== REPORTS ==============
with tab5:
    st.markdown("## 📈 রিপোর্ট ও বিশ্লেষণ")
    
    if st.session_state.demo_mode:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("মোট গ্রাহক", "5", "↑ ২ এই মাসে")
        
        with col2:
            st.metric("মোট চালান", "৳25,000", "↑ ৳8,000")
        
        with col3:
            st.metric("মোট খরচ", "৳5,800", "↓ ৳200")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 খরচ বিভাজন")
            
            expense_summary = {
                'বিভাগ': ['কাঁচামাল', 'ভাড়া', 'বিদ্যুৎ', 'অন্যান্য'],
                'পরিমাণ': [3000, 2000, 800, 1000]
            }
            
            df_expense = pd.DataFrame(expense_summary)
            st.bar_chart(df_expense.set_index('বিভাগ'))
        
        with col2:
            st.markdown("### 📊 গ্রাহক শীর্ষ ৫")
            
            customer_data = {
                'গ্রাহক নাম': ['রহিম দোকান', 'আলী স্টোর', 'ফারিহা অফিস', 'করিম সেবা', 'জামিলা শপ'],
                'মোট আয়': [10000, 8000, 5000, 2000, 1000]
            }
            
            df_customer = pd.DataFrame(customer_data)
            st.bar_chart(df_customer.set_index('গ্রাহক নাম'))
        
        st.markdown("---")
        
        st.markdown("### 📋 সংক্ষিপ্ত সারাংশ")
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.markdown("""
            **মোট আয়**  
            ৳25,000
            """)
        
        with summary_col2:
            st.markdown("""
            **মোট খরচ**  
            ৳5,800
            """)
        
        with summary_col3:
            st.markdown("""
            **নেট লাভ**  
            ৳19,200
            """)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 CSV এ এক্সপোর্ট করুন", use_container_width=True):
                st.success("✅ ডেটা এক্সপোর্ট প্রস্তুত")
        
        with col2:
            if st.button("🖨️ রিপোর্ট প্রিন্ট করুন", use_container_width=True):
                st.success("✅ প্রিন্ট প্রস্তুত")
    else:
        st.info("📌 Google Sheets সংযুক্ত করলে রিপোর্ট দেখা যাবে")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
    <p><strong>© 2024 H M Computer & Printers</strong></p>
    <p>সমস্ত অধিকার সংরক্ষিত</p>
    <p style='font-size: 0.9em; margin-top: 10px;'>
        📞 01725-466228 | 01670-914931<br>
        📧 hmcomputerp@gmail.com<br>
        📍 চান্দিনা, কুমিল্লা
    </p>
</div>
""", unsafe_allow_html=True)
