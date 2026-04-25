import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="مقاصد الطلاب", page_icon="🕌", layout="wide")

# 2. التنسيق الإسلامي الفخم (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Aref+Ruqaa:wght@400;700&display=swap');
    .stApp {
        background-color: #f4f7f1;
        background-image: url("https://www.transparenttextures.com/patterns/arabesque.png");
    }
    html, body, [class*="css"]  {
        font-family: 'Amiri', serif;
        text-align: right;
    }
    .bright-title {
        font-family: 'Aref Ruqaa', serif;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 15px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .custom-card {
        background: white; padding: 15px; border-radius: 12px;
        border-right: 8px solid #1e4d2b; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: #1e4d2b; padding: 8px; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. تهيئة مخازن البيانات (Session State) - لضمان عدم ضياع البيانات
if 'books_db' not in st.session_state: st.session_state.books_db = []
if 'messages' not in st.session_state: st.session_state.messages = []
if 'students_list' not in st.session_state: st.session_state.students_list = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'user_info' not in st.session_state: st.session_state.user_info = {}

# 4. منطق تسجيل الدخول
if not st.session_state.logged_in:
    st.markdown('<div class="bright-title">مَقَاصِدُ الطُلَّابِ فِي الأدَبِ وَ الإِعْرَابِ</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_stu, tab_sup = st.tabs(["🎓 واجهة الطالب", "🔑 واجهة المشرف"])
        
        with tab_stu:
            with st.form("stu_login"):
                n = st.text_input("الاسم الثلاثي")
                l = st.selectbox("الصف الدراسي", ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الرابع العلمي", "الرابع الأدبي", "الخامس العلمي", "الخامس الأدبي", "السادس العلمي", "السادس الأدبي"])
                if st.form_submit_button("دخول"):
                    if n:
                        st.session_state.logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.user_info = {"الاسم": n, "الصف": l}
                        # إضافة الطالب للقائمة إذا لم يكن موجوداً
                        if not any(s['الاسم'] == n for s in st.session_state.students_list):
                            st.session_state.students_list.append({"الاسم": n, "الصف": l})
                        st.rerun()
                    else: st.error("أدخل الاسم رجاءً")

        with tab_sup:
            with st.form("sup_login"):
                u = st.text_input("المشرف")
                p = st.text_input("كلمة المرور", type="password")
                if st.form_submit_button("دخول"):
                    if u == "admin" and p == "12345":
                        st.session_state.logged_in = True
                        st.session_state.user_role = "supervisor"
                        st.rerun()
                    else: st.error("خطأ في البيانات")

# 5. واجهة التطبيق بعد الدخول
else:
    with st.sidebar:
        st.markdown(f"<h2 style='color:#ffd700; text-align:center;'>{st.session_state.user_role.upper()}</h2>", unsafe_allow_html=True)
        st.write(f"👤 {st.session_state.user_info.get('الاسم', 'المشرف')}")
        if st.button("تسجيل الخروج"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown('<div class="bright-title" style="font-size: 2.2rem;">مَقَاصِدُ الطُلَّابِ فِي الأدَبِ وَ الإِعْرَابِ</div>', unsafe_allow_html=True)

    # تبويبات المشرف
    if st.session_state.user_role == "supervisor":
        t1, t2, t3, t4 = st.tabs(["📚 إدارة المكتبة", "📩 رسائل الطلاب", "👥 سجل الأسماء", "💬 نقاش"])
        
        with t1:
            st.subheader("إضافة كتب جديدة")
            with st.form("upload_form", clear_on_submit=True):
                name = st.text_input("عنوان الكتاب")
                file = st.file_uploader("ملف PDF", type="pdf")
                mode = st.radio("الوضع", ["قراءة فقط", "قراءة وتحميل"])
                if st.form_submit_button("نشر الكتاب"):
                    if name and file:
                        st.session_state.books_db.append({"name": name, "data": file.getvalue(), "can_down": "تحميل" in mode})
                        st.success("تم الحفظ")
        
        with t2:
            st.subheader("رسائل الطلاب الواردة")
            for m in st.session_state.messages:
                with st.container():
                    st.markdown(f"<div class='custom-card'><b>{m['sender']} ({m['class']}):</b><br>{m['text']}</div>", unsafe_allow_html=True)

        with t3:
            st.subheader("قائمة الطلاب المسجلين")
            if st.session_state.students_list:
                st.table(pd.DataFrame(st.session_state.students_list))
            else: st.warning("لا يوجد طلاب حالياً")

    # تبويبات الطالب
    else:
        t1, t2, t3 = st.tabs(["📚 المكتبة", "📝 سؤال للمشرف", "💬 نقاش"])
        
        with t1:
            st.subheader("الكتب المتاحة")
            for b in st.session_state.books_db:
                with st.container():
                    st.markdown(f"<div class='custom-card'><h3>📖 {b['name']}</h3></div>", unsafe_allow_html=True)
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.download_button("👁️ فتح/قراءة", data=b['data'], file_name=f"{b['name']}.pdf", mime="application/pdf", key=f"v_{b['name']}")
                    with col_b:
                        if b['can_down']:
                            st.download_button("📥 تحميل", data=b['data'], file_name=f"{b['name']}.pdf", key=f"d_{b['name']}")
        
        with t2:
            with st.form("send_msg"):
                msg_txt = st.text_area("اكتب سؤالك")
                if st.form_submit_button("إرسال"):
                    st.session_state.messages.append({
                        "sender": st.session_state.user_info['الاسم'],
                        "class": st.session_state.user_info['الصف'],
                        "text": msg_txt
                    })
                    st.success("تم الإرسال")
