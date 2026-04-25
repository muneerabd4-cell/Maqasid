import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="مقاصد الطلاب", page_icon="🕌", layout="wide")

# 2. التنسيق الإسلامي الاحترافي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Aref+Ruqaa:wght@400;700&display=swap');

    /* خلفية التطبيق بألوان إسلامية هادئة وزخارف */
    .stApp {
        background-color: #f4f7f1;
        background-image: url("https://www.transparenttextures.com/patterns/arabesque.png");
    }

    /* الخطوط العربية */
    html, body, [class*="css"]  {
        font-family: 'Amiri', serif;
        text-align: right;
    }

    /* العنوان البراق - ذهبي إسلامي */
    .bright-title {
        font-family: 'Aref Ruqaa', serif;
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 20px;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* تنسيق التبويبات والقوائم */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1e4d2b; /* أخضر غامق إسلامي */
        padding: 10px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-family: 'Amiri', serif;
        font-size: 1.2rem;
    }

    /* كروت الكتب والرسائل */
    .custom-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-right: 10px solid #1e4d2b;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* القائمة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #1e4d2b;
        color: white;
    }
    .sidebar-text { color: #ffd700 !important; font-family: 'Aref Ruqaa', serif; font-size: 1.5rem; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة الحالة (Session State) لتخزين البيانات
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_info = {}
if 'books_db' not in st.session_state:
    st.session_state.books_db = []
if 'messages' not in st.session_state:
    st.session_state.messages = [] # تخزين رسائل الطلاب للرد عليها
if 'students_list' not in st.session_state:
    st.session_state.students_list = [] # قاعدة بيانات الطلاب المسجلين

# 4. واجهة تسجيل الدخول
if not st.session_state.logged_in:
    st.markdown('<div class="bright-title">مَقَاصِدُ الطُلَّابِ فِي الأدَبِ وَ الإِعْرَابِ</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_stu, tab_sup = st.tabs(["🎓 واجهة الطالب", "🔑 واجهة المشرف"])

        with tab_stu:
            with st.form("student_login"):
                n = st.text_input("الاسم الثلاثي")
                l = st.selectbox("الصف الدراسي", ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الرابع العلمي", "الرابع الأدبي", "الخامس العلمي", "الخامس الأدبي", "السادس العلمي", "السادس الأدبي"])
                if st.form_submit_button("دخول المنصة"):
                    if n:
                        st.session_state.logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.user_info = {"الاسم": n, "الصف": l}
                        # إضافة الطالب لقائمة الأسماء لدى المشرف
                        st.session_state.students_list.append({"الاسم": n, "الصف": l})
                        st.rerun()
                    else: st.error("يرجى كتابة اسمك")

        with tab_sup:
            with st.form("supervisor_login"):
                u = st.text_input("اسم المستخدم (المشرف)")
                p = st.text_input("كلمة المرور", type="password")
                if st.form_submit_button("دخول المشرف"):
                    if u == "admin" and p == "12345":
                        st.session_state.logged_in = True
                        st.session_state.user_role = "supervisor"
                        st.rerun()
                    else: st.error("البيانات خاطئة")

# 5. الواجهة الرئيسية بعد الدخول
else:
    with st.sidebar:
        st.markdown('<div class="sidebar-text">مَقَاصِدُ الطُلَّابِ</div>', unsafe_allow_html=True)
        st.markdown("---")
        if st.session_state.user_role == "supervisor":
            st.write("🟢 مرحباً بك أيها المشرف")
        else:
            st.write(f"👤 الطالب: {st.session_state.user_info['الاسم']}")
            st.write(f"🏫 الصف: {st.session_state.user_info['الصف']}")
        
        if st.button("تسجيل الخروج"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown('<div class="bright-title" style="font-size: 2.5rem;">مَقَاصِدُ الطُلَّابِ فِي الأدَبِ وَ الإِعْرَابِ</div>', unsafe_allow_html=True)

    # التبويبات بناءً على الصلاحيات
    if st.session_state.user_role == "supervisor":
        tabs = st.tabs(["📚 إدارة المكتبة", "📩 الرد على الرسائل", "👥 سجل الطلاب", "💬 المحادثة العامة"])
    else:
        tabs = st.tabs(["📚 المكتبة العربية", "📝 أرسل سؤالك", "💬 المحادثة العامة"])

    # --- تبويب المكتبة ---
    with tabs[0]:
        st.header("📚 مكتبة العلوم العربية")
        if st.session_state.user_role == "supervisor":
            with st.expander("➕ رفع كتاب جديد"):
                b_name = st.text_input("اسم الكتاب")
                b_file = st.file_uploader("اختر ملف PDF", type="pdf")
                b_opt = st.radio("الصلاحية:", ["للقراءة فقط", "للقراءة والتحميل"])
                if st.button("نشر الآن"):
                    if b_name and b_file:
                        st.session_state.books_db.append({
                            "name": b_name, "data": b_file.getvalue(), 
                            "download": True if "تحميل" in b_opt else False
                        })
                        st.success("تم النشر")

        for book in st.session_state.books_db:
            with st.container():
                st.markdown(f'<div class="custom-card"><h3>📖 {book["name"]}</h3></div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    # ميزة القراءة (حل مشكلة عدم الفتح بتوفير رابط مباشر)
                    st.download_button(f"👁️ فتح وقراءة {book['name']}", data=book['data'], file_name=f"{book['name']}.pdf", mime="application/pdf")
                with c2:
                    if book['download'] or st.session_state.user_role == "supervisor":
                        st.download_button(f"📥 تحميل {book['name']}", data=book['data'], file_name=f"{book['name']}.pdf", key=f"d_{book['name']}")
                    else: st.warning("التحميل معطل بطلب من المشرف")

    # --- تبويب الرسائل / الردود ---
    if st.session_state.user_role == "supervisor":
        with tabs[1]:
            st.header("📩 بريد الطلاب")
            if not st.session_state.messages: st.write("لا توجد رسائل جديدة.")
            for i, msg in enumerate(st.session_state.messages):
                with st.container():
                    st.markdown(f'<div class="custom-card"><b>من: {msg["student"]} ({msg["class"]})</b><br>{msg["text"]}</div>', unsafe_allow_html=True)
                    reply = st.text_area(f"الرد على {msg['student']}", key=f"rep_{i}")
                    if st.button("إرسال الرد", key=f"btn_{i}"):
                        st.success(f"تم إرسال الرد إلى {msg['student']}")

        with tabs[2]:
            st.header("👥 سجل الطلاب المسجلين")
            filter_class = st.selectbox("تصفية حسب الصف:", ["الكل", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الرابع العلمي", "الرابع الأدبي", "الخامس العلمي", "الخامس الأدبي", "السادس العلمي", "السادس الأدبي"])
            
            df_students = pd.DataFrame(st.session_state.students_list)
            if not df_students.empty:
                if filter_class != "الكل":
                    df_students = df_students[df_students['الصف'] == filter_class]
                st.table(df_students)
            else: st.info("لا يوجد طلاب مسجلون حالياً")
            
    else:
        with tabs[1]:
            st.header("📝 أرسل سؤالك للمشرف")
            with st.form("msg_form"):
                txt = st.text_area("اكتب سؤالك هنا بوضوح...")
                if st.form_submit_button("إرسال السؤال"):
                    st.session_state.messages.append({
                        "student": st.session_state.user_info['الاسم'],
                        "class": st.session_state.user_info['الصف'],
                        "text": txt
                    })
                    st.success("تم إرسال سؤالك للمشرف بنجاح")

    # --- تبويب المحادثة العامة ---
    with tabs[-1]:
        st.header("💬 غرفة النقاش الجماعي")
        st.chat_message("assistant").write("مرحباً بكم في مجلس الأدب والإعراب..")
        if chat_input := st.chat_input("اكتب مشاركتك هنا..."):
            st.chat_message("user").write(chat_input)
