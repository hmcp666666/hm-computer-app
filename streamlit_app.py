import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="HM Computer & Printers",
    page_icon="💼",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .purple { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .green { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
    .yellow { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
    .red { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>💼 H M Computer & Printers</h1>
    <p>ব্যবসা ব্যবস্থাপনা সিস্টেম | Business Management System</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'customers_list' not in st.session_state:
    st.session_state.customers_list = []
if 'invoices_list' not in st.session_state:
    st.session_state.invoices_list = []
if 'expenses_list' not in st.session_state:
    st.session_state.expenses_list = []

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 ড্যাশবোর্ড",
    "👥 গ্রাহক",
    "📋 চালান",
    "💰 খরচ",
    "📈 রিপোর্ট"
])

# ============ TAB 1: DASHBOARD ============
with tab1:
    st.markdown("## 📊 ব্যবসা ড্যাশবোর্ড")
    
    # Sample metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card purple">
            <div style="font-size: 0.9em; opacity: 0.9;">মোট গ্রাহক</div>
            <div style="font-size: 2.5em; margin-top: 10px;">{len(st.session_state.customers_list)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_income = sum([inv.get('total', 0) for inv in st.session_state.invoices_list])
        st.markdown(f"""
        <div class="metric-card green">
            <div style="font-size: 0.9em; opacity: 0.9;">মোট আয়</div>
            <div style="font-size: 2.5em; margin-top: 10px;">৳{total_income:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_expense = sum([exp.get('amount', 0) for exp in st.session_state.expenses_list])
        st.markdown(f"""
        <div class="metric-card yellow">
            <div style="font-size: 0.9em; opacity: 0.9;">মোট খরচ</div>
            <div style="font-size: 2.5em; margin-top: 10px;">৳{total_expense:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        profit = total_income - total_expense
        st.markdown(f"""
        <div class="metric-card red">
            <div style="font-size: 0.9em; opacity: 0.9;">নেট লাভ</div>
            <div style="font-size: 2.5em; margin-top: 10px;">৳{profit:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 আয় ও খরচ")
        chart_data = pd.DataFrame({
            'ক্যাটাগরি': ['আয়', 'খরচ'],
            'পরিমাণ': [total_income, total_expense]
        })
        st.bar_chart(chart_data.set_index('ক্যাটাগরি'), color=['#10b981', '#f59e0b'])
    
    with col2:
        st.markdown("#### 💰 বিক্রয় প্রবণতা")
        if st.session_state.invoices_list:
            df_inv = pd.DataFrame(st.session_state.invoices_list)
            st.line_chart(df_inv[['date', 'total']].set_index('date'))
        else:
            st.info("📌 ডেটা যোগ করুন দেখতে")

# ============ TAB 2: CUSTOMERS ============
with tab2:
    st.markdown("## 👥 গ্রাহক ব্যবস্থাপনা")
    
    col1, col2 = st.columns([4, 1])
    
    with col2:
        add_customer = st.button("➕ গ্রাহক যোগ করুন", key="btn_add_customer", use_container_width=True)
    
    if add_customer:
        st.markdown("### নতুন গ্রাহক যোগ করুন")
        
        with st.form("form_customer", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                cust_name = st.text_input("নাম *", key="cust_name")
                cust_phone = st.text_input("ফোন *", key="cust_phone")
            
            with col2:
                cust_email = st.text_input("ইমেইল", key="cust_email")
                cust_address = st.text_area("ঠিকানা", key="cust_address", height=80)
            
            submit_btn = st.form_submit_button("💾 সংরক্ষণ করুন")
            
            if submit_btn and cust_name and cust_phone:
                st.session_state.customers_list.append({
                    'name': cust_name,
                    'phone': cust_phone,
                    'email': cust_email,
                    'address': cust_address,
                    'date': datetime.now().strftime("%Y-%m-%d")
                })
                st.success(f"✅ {cust_name} যোগ হয়েছে!")
                st.rerun()
    
    st.markdown("---")
    
    if st.session_state.customers_list:
        st.markdown(f"### মোট গ্রাহক: {len(st.session_state.customers_list)}")
        df_cust = pd.DataFrame(st.session_state.customers_list)
        st.dataframe(df_cust, use_container_width=True, hide_index=True)
    else:
        st.info("📌 প্রথম গ্রাহক যোগ করুন")

# ============ TAB 3: INVOICES ============
with tab3:
    st.markdown("## 📋 চালান ব্যবস্থাপনা")
    
    col1, col2 = st.columns([4, 1])
    
    with col2:
        add_invoice = st.button("➕ চালান তৈরি করুন", key="btn_add_invoice", use_container_width=True)
    
    if add_invoice:
        st.markdown("### নতুন চালান তৈরি করুন")
        
        with st.form("form_invoice", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                inv_customer = st.text_input("গ্রাহক নাম *", key="inv_customer")
                inv_items = st.text_input("পণ্য/সেবা *", key="inv_items")
                inv_quantity = st.number_input("পরিমাণ", min_value=1, key="inv_quantity")
            
            with col2:
                inv_price = st.number_input("মূল্য (টাকা) *", min_value=0.0, key="inv_price")
                inv_date = st.date_input("তারিখ", key="inv_date")
                inv_status = st.selectbox("অবস্থা", ["অপেক্ষারত", "প্রদত্ত"], key="inv_status")
            
            submit_inv = st.form_submit_button("💾 চালান সংরক্ষণ করুন")
            
            if submit_inv and inv_customer and inv_items:
                st.session_state.invoices_list.append({
                    'customer': inv_customer,
                    'items': inv_items,
                    'quantity': inv_quantity,
                    'price': inv_price,
                    'total': inv_quantity * inv_price,
                    'status': inv_status,
                    'date': inv_date.strftime("%Y-%m-%d")
                })
                st.success("✅ চালান সংরক্ষণ হয়েছে!")
                st.rerun()
    
    st.markdown("---")
    
    if st.session_state.invoices_list:
        st.markdown(f"### মোট চালান: {len(st.session_state.invoices_list)}")
        df_inv = pd.DataFrame(st.session_state.invoices_list)
        st.dataframe(df_inv, use_container_width=True, hide_index=True)
    else:
        st.info("📌 প্রথম চালান তৈরি করুন")

# ============ TAB 4: EXPENSES ============
with tab4:
    st.markdown("## 💰 খরচ ট্র্যাকিং")
    
    col1, col2 = st.columns([4, 1])
    
    with col2:
        add_expense = st.button("➕ খরচ যোগ করুন", key="btn_add_expense", use_container_width=True)
    
    if add_expense:
        st.markdown("### নতুন খরচ রেকর্ড করুন")
        
        with st.form("form_expense", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                exp_desc = st.text_input("বর্ণনা *", key="exp_desc")
                exp_category = st.selectbox("বিভাগ *", [
                    "কাঁচামাল", "বেতন", "ভাড়া", "বিদ্যুৎ",
                    "মেরামত", "পরিবহন", "অন্যান্য"
                ], key="exp_category")
            
            with col2:
                exp_amount = st.number_input("পরিমাণ (টাকা) *", min_value=0.0, key="exp_amount")
                exp_date = st.date_input("তারিখ", key="exp_date")
            
            submit_exp = st.form_submit_button("💾 সংরক্ষণ করুন")
            
            if submit_exp and exp_desc:
                st.session_state.expenses_list.append({
                    'description': exp_desc,
                    'category': exp_category,
                    'amount': exp_amount,
                    'date': exp_date.strftime("%Y-%m-%d")
                })
                st.success("✅ খরচ সংরক্ষণ হয়েছে!")
                st.rerun()
    
    st.markdown("---")
    
    if st.session_state.expenses_list:
        st.markdown(f"### মোট খরচ রেকর্ড: {len(st.session_state.expenses_list)}")
        df_exp = pd.DataFrame(st.session_state.expenses_list)
        st.dataframe(df_exp, use_container_width=True, hide_index=True)
    else:
        st.info("📌 প্রথম খরচ যোগ করুন")

# ============ TAB 5: REPORTS ============
with tab5:
    st.markdown("## 📈 রিপোর্ট ও বিশ্লেষণ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("মোট গ্রাহক", len(st.session_state.customers_list))
    
    with col2:
        total_inv = sum([inv.get('total', 0) for inv in st.session_state.invoices_list])
        st.metric("মোট চালান", f"৳{total_inv:,}")
    
    with col3:
        total_exp = sum([exp.get('amount', 0) for exp in st.session_state.expenses_list])
        st.metric("মোট খরচ", f"৳{total_exp:,}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 খরচ বিভাজন")
        if st.session_state.expenses_list:
            df_exp = pd.DataFrame(st.session_state.expenses_list)
            expense_summary = df_exp.groupby('category')['amount'].sum()
            st.bar_chart(expense_summary)
        else:
            st.info("📌 খরচ ডেটা পেতে খরচ যোগ করুন")
    
    with col2:
        st.markdown("### 📊 সারাংশ")
        total_income = sum([inv.get('total', 0) for inv in st.session_state.invoices_list])
        total_expense = sum([exp.get('amount', 0) for exp in st.session_state.expenses_list])
        profit = total_income - total_expense
        
        st.markdown(f"""
        **মোট আয়:** ৳{total_income:,}  
        **মোট খরচ:** ৳{total_expense:,}  
        **নেট লাভ:** ৳{profit:,}
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
    <p><strong>© 2024 H M Computer & Printers</strong></p>
    <p>সর্বস্বত্ব সংরক্ষিত | All Rights Reserved</p>
    <p style='font-size: 0.85em;'>
        📞 01725-466228 | 01670-914931<br>
        📧 hmcomputerp@gmail.com
    </p>
</div>
""", unsafe_allow_html=True)
