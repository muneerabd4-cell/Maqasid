import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="منصة مقاصد الطلاب", page_icon="🎓", layout="wide")

# تهيئة المتغيرات
if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.role = None

# 1. شاشة الدخول
if not st.session_state.auth:
    st.title("🔐 بوابة دخول المنصة")
    role = st.selectbox("تسجيل الدخول كـ:", ["طالب", "مطور (المشرف)"])
    
    if role == "طالب":
        with st.form("student_login"):
            st.text_input("الاسم الثلاثي")
            st.text_input("رقم الهاتف")
            st.selectbox("المرحلة الدراسية", ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط"])
            if st.form_submit_button("دخول الطالب"):
                st.session_state.auth = True
                st.session_state.role = "student"
                st.rerun()
    else:
        pin = st.text_input("رمز المشرف", type="password")
        if st.button("دخول المطور"):
            if pin == "1234": # رمز المشرف الافتراضي
                st.session_state.auth = True
                st.session_state.role = "admin"
                st.rerun()

# 2. واجهة المطور
elif st.session_state.role == "admin":
    st.sidebar.title("🛠 لوحة المطور")
    menu = st.sidebar.radio("القائمة:", ["إعدادات النظام", "رفع ملفات", "توليد أسئلة"])
    
    if menu == "إعدادات النظام":
        st.header("⚙️ التحكم في التطبيق")
        st.write("هنا يمكنك تغيير الرموز وإدارة صلاحيات الدخول.")
        
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

# 3. واجهة الطالب
else:
    st.sidebar.title("👨‍🎓 بوابة الطالب")
    menu = st.sidebar.radio("القائمة:", ["إعراب القرآن", "ديوان العرب", "ملفات PDF", "اختباراتي"])
    
    st.header(f"أهلاً بك في قسم {menu}")
    st.info("سيظهر المحتوى هنا بمجرد رفعه من قبل المشرف.")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
