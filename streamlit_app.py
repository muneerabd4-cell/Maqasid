import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# --- إعدادات التهيئة والتحكم (Settings Controller) ---
if 'app_config' not in st.session_state:
    st.session_state.app_config = {
        "name": "منصة مقاصد الطلاب",
        "bg_color": "#ffffff",
        "font_size": 18,
        "cover_image": None
    }

# تطبيق إعدادات المطور على واجهة التطبيق
st.set_page_config(page_title=st.session_state.app_config["name"], layout="wide")

# --- نظام الجلسات (Session State) ---
if 'auth' not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "user_data": {}, "otp_sent": False, "otp_verified": False
    })

# --- دالة التحقق من الهاتف (SMS Verification Simulation) ---
def verify_phone(phone):
    # هنا يتم الربط مع خدمة مثل Twilio أو Firebase
    # للتبسيط سنفترض أن الكود هو 1234
    st.session_state.otp_sent = True
    st.info(f"تم إرسال كود التحقق إلى {phone} (تجريبياً: 1234)")

# --- واجهة الدخول المختلطة ---
def login_screen():
    st.title(st.session_state.app_config["name"])
    tab1, tab2 = st.tabs(["👨‍🎓 بوابة الطالب", "🔐 بوابة المشرف"])

    with tab1:
        name = st.text_input("اسم الطالب الثلاثي")
        grade = st.selectbox("الصف الدراسي", [
            "الأول متوسط", "الثاني المتوسط", "الثالث المتوسط", 
            "الرابع العلمي", "الرابع الأدبي", "الخامس العلمي", 
            "الخامس الأدبي", "السادس العلمي", "السادس الأدبي"
        ])
        phone = st.text_input("رقم الهاتف (مثال: +964...)")
        
        if not st.session_state.otp_sent:
            if st.button("إرسال كود التحقق"):
                verify_phone(phone)
        else:
            otp = st.text_input("أدخل كود التحقق المستلم")
            if st.button("تأكيد الدخول"):
                if otp == "1234":
                    st.session_state.update({"auth": True, "role": "student", "user_data": {"name": name, "grade": grade, "phone": phone}})
                    st.rerun()

    with tab2:
        admin_user = st.text_input("اسم المشرف")
        admin_pass = st.text_input("كلمة المرور", type="password")
        if st.button("دخول المشرف"):
            if admin_pass == "admin2026": # كلمة السر الافتراضية
                st.session_state.update({"auth": True, "role": "admin"})
                st.rerun()

# --- لوحة تحكم المشرف (Admin Dashboard) ---
def admin_interface():
    st.markdown(f"### 🛠 لوحة تحكم: {st.session_state.app_config['name']}")
    menu = st.tabs([
        "إعراب القرآن", "ديوان العرب", "توليد الأسئلة AI", "البث المباشر", 
        "الرسائل", "إدارة الأعضاء", "الرفع", "المشرفين", "⚙️ الإعدادات"
    ])

    with menu[2]: # توليد الأسئلة
        st.header("🤖 توليد بالذكاء الاصطناعي (Gemini)")
        topic = st.text_input("موضوع الاختبار")
        num_q = st.number_input("عدد الأسئلة", 1, 50)
        q_type = st.radio("نوع الإجابة", ["خيارات متعددة", "ردود نصية"])
        if st.button("توليد ونشر"):
            st.success("تم التوليد والنشر لصفحة الطلاب")

    with menu[3]: # البث المباشر
        st.header("📺 غرفة البث المباشر")
        st.radio("نوع البث", ["صوت فقط", "صوت وصورة"])
        st.button("بدء البث المباشر")
        st.warning("يتطلب هذا القسم ربط خدمة WebRTC أو Zoom SDK")

    with menu[5]: # إدارة الأعضاء
        st.header("👥 قاعدة بيانات الطلاب")
        # مثال لبيانات طالب
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("الاسم: أحمد علي")
            if st.button("📞 اتصال"): pass
        with col2:
            st.write("المرحلة: السادس العلمي")
            st.link_button("💬 واتساب", "https://wa.me/9640000000")
        with col3:
            st.button("📄 ملف الطالب")

    with menu[8]: # الإعدادات
        st.header("⚙️ السيطرة الكاملة")
        st.session_state.app_config["name"] = st.text_input("اسم التطبيق", st.session_state.app_config["name"])
        st.color_picker("لون الخلفية العام", "#ffffff")
        if st.button("حفظ الإعدادات"): st.rerun()

# --- واجهة الطالب (Student Interface) ---
def student_interface():
    st.title(f"مرحباً، {st.session_state.user_data['name']}")
    
    # التبويبات في الأسفل (محاكاة عبر الأعمدة)
    content_area = st.container(height=500)
    
    st.markdown("---")
    cols = st.columns(6)
    with cols[0]: 
        if st.button("📖 القرآن"): st.session_state.student_view = "quran"
    with cols[1]:
        if st.button("📜 الديوان"): st.session_state.student_view = "poetry"
    with cols[2]:
        if st.button("📁 ملفات"): st.session_state.student_view = "files"
    with cols[3]:
        if st.button("🎥 وسائط"): st.session_state.student_view = "media"
    with cols[4]:
        if st.button("💬 مراسلة"): st.session_state.student_view = "chat"
    with cols[5]:
        if st.button("📞 الرد"): st.session_state.student_view = "call"

    # منطقة العرض بناءً على اختيار التبويب السفلي
    view = st.session_state.get("student_view", "quran")
    with content_area:
        if view == "quran": st.header("📖 إعراب القرآن الكريم")
        elif view == "poetry": st.header("📜 ديوان العرب")
        elif view == "call": st.header("📞 استقبال البث / الاتصال")

# --- تشغيل التطبيق ---
if not st.session_state.auth:
    login_screen()
else:
    if st.session_state.role == "admin":
        admin_interface()
    else:
        student_interface()
