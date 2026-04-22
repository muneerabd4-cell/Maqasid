import streamlit as st
import google.generativeai as genai

# إعدادات المنصة
st.set_page_config(page_title="منصة مقاصد الطلاب", layout="wide")

# رمز المطور (المشرف)
ADMIN_PIN = "1234"

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.role = None

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.title("🎓 منصة مقاصد الطلاب التعليمية")
    role = st.radio("تسجيل الدخول كـ:", ["طالب", "مطور (المشرف)"])
    if role == "طالب":
        name = st.text_input("الاسم")
        if st.button("دخول"):
            st.session_state.auth, st.session_state.role = True, "student"
            st.rerun()
    else:
        pin = st.text_input("رمز الدخول", type="password")
        if st.button("دخول المشرف"):
            if pin == ADMIN_PIN:
                st.session_state.auth, st.session_state.role = True, "admin"
                st.rerun()

# --- واجهة المطور (المشرف) ---
elif st.session_state.role == "admin":
    st.sidebar.title("🛠 لوحة التحكم")
    task = st.sidebar.selectbox("اختر القسم العملي:", 
        ["إدارة الأعضاء", "رفع الوسائط والملفات", "توليد أسئلة بالذكاء الاصطناعي", "إضافة إعراب ودواوين"])

    if task == "إدارة الأعضاء":
        st.header("👥 قائمة الطلاب المسجلين")
        st.write("هنا ستظهر قائمة بأسماء الطلاب الذين سجلوا دخولهم.")

    elif task == "رفع الوسائط والملفات":
        st.header("📁 مركز رفع الوسائط (PDF/فيديو)")
        file = st.file_uploader("اختر الملف", type=['pdf', 'mp4', 'png', 'jpg'])
        if st.button("نشر للمكتبة"): st.success("تم النشر بنجاح")

    elif task == "توليد أسئلة بالذكاء الاصطناعي":
        st.header("🤖 مولد الاختبارات الذكي")
        topic = st.text_input("المادة العلميّة (مثلاً: إعراب المبتدأ)")
        if st.button("توليد اختبار"):
            st.info("جاري التواصل مع الذكاء الاصطناعي...")
            # هنا نربط بمفتاح Gemini لاحقاً

# --- واجهة الطالب (العرض) ---
else:
    st.sidebar.title("📖 قائمة الطالب")
    view = st.sidebar.radio("انتقل إلى:", 
        ["إعراب القرآن", "ديوان العرب", "مكتبة الوسائط", "ملخصاتي", "الاختبارات"])

    if view == "إعراب القرآن":
        st.header("📖 المصحف المعرب")
        st.write("اختر السورة لعرض الإعراب (يتم رفعه من لوحة المطور)")

    elif view == "ديوان العرب":
        st.header("📜 ديوان العرب (قصائد)")
        st.write("تصفح المعلقات والقصائد المختارة.")

    elif view == "مكتبة الوسائط":
        st.header("🎥 الوسائط والملفات التعليمية")
        st.write("هنا تظهر ملفات الـ PDF والدروس المرئية.")

if st.sidebar.button("تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()
