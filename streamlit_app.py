import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مقاصد الطلاب", page_icon="📖", layout="wide")

# 2. إضافة التنسيقات الجمالية (CSS) لاسم التطبيق البراق والواجهة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&display=swap');

    /* تنسيق العنوان البراق المتحرك */
    .bright-title {
        font-family: 'Amiri', serif;
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        background-size: 200% auto;
        color: #fff;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        padding: 10px;
        margin-bottom: 20px;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* تنسيق العنوان في القائمة الجانبية */
    .sidebar-title {
        font-family: 'Amiri', serif;
        font-size: 1.5rem;
        color: #FFD700;
        text-align: center;
        border-bottom: 1px solid #FFD700;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    /* كروت الكتب */
    .book-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #ffffff;
        border-right: 8px solid #FFD700;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_info = {}
if 'books_db' not in st.session_state:
    st.session_state.books_db = []

# 4. واجهة تسجيل الدخول
if not st.session_state.logged_in:
    st.markdown('<div class="bright-title">مَقَاصِدُ الطُلَّابِ فِي الأدَبِ وَ الإِعْرَابِ</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_stu, tab_sup = st.tabs(["🎓 دخول الطالب", "🔑 دخول المشرف"])

        with tab_stu:
            with st.form("student_login"):
                n = st.text_input("الاسم الثلاثي")
                # تعديل: تغيير المرحلة إلى الصف الدراسي وإضافة الخيارات الجديدة
                l = st.selectbox("الصف الدراسي", [
                    "الأول المتوسط", 
                    "الثاني المتوسط", 
                    "الثالث المتوسط", 
                    "الرابع العلمي", 
                    "الرابع الأدبي", 
                    "الخامس العلمي", 
                    "الخامس الأدبي", 
                    "السادس العلمي", 
                    "السادس الأدبي"
                ])
                if st.form_submit_button("دخول المنصة"):
                    if n:
                        st.session_state.logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.user_info = {"الاسم": n, "الصف": l}
                        st.rerun()
                    else:
                        st.error("يرجى إدخال الاسم")

        with tab_sup:
            with st.form("supervisor_login"):
                u = st.text_input("اسم المستخدم")
                p = st.text_input("كلمة المرور", type="password")
                if st.form_submit_button("تسجيل دخول المشرف"):
                    if u == "memom" and p == "873422": 
                        st.session_state.logged_in = True
                        st.session_state.user_role = "supervisor"
                        st.rerun()
                    else:
                        st.error("بيانات المشرف غير صحيحة")

# 5. الواجهة الرئيسية بعد الدخول
else:
    with st.sidebar:
        st.markdown('<div class="sidebar-title">مَقَاصِدُ الطُلَّابِ</div>', unsafe_allow_html=True)
        if st.session_state.user_role == "supervisor":
            st.success("مرحباً بك أيها المشرف")
        else:
            st.write(f"👤 **الطالب:** {st.session_state.user_info['الاسم']}")
            st.write(f"🏫 **الصف:** {st.session_state.user_info['الصف']}")
        
        st.markdown("---")
        if st.button("تسجيل الخروج"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown('<div class="bright-title" style="font-size: 2.5rem;">مَقَاصِدُ الطُلَّابِ فِي الأدَبِ وَ الإِعْرَابِ</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📚 مكتبة الكتب العربية", "💬 غرفة النقاش", "📢 الإعلانات"])

    with tab1:
        st.header("مكتبة الكتب العربية")
        
        if st.session_state.user_role == "supervisor":
            with st.expander("➕ إضافة كتاب جديد (للمشرف فقط)"):
                b_name = st.text_input("اسم الكتاب أو المخطوطة")
                b_file = st.file_uploader("ارفع الكتاب بصيغة PDF", type="pdf")
                b_opt = st.radio("خيارات الطالب:", ["للقراءة فقط", "للقراءة والتحميل"])
                if st.button("نشر الكتاب"):
                    if b_name and b_file:
                        st.session_state.books_db.append({
                            "name": b_name,
                            "data": b_file.getvalue(),
                            "download": True if "والتحميل" in b_opt else False
                        })
                        st.success("تمت إضافة الكتاب للمكتبة بنجاح!")
                    else:
                        st.error("يرجى إكمال بيانات الكتاب")

        st.markdown("---")
        if not st.session_state.books_db:
            st.info("المكتبة خالية حالياً، بانتظار رفع الكتب من قبل المشرف.")
        else:
            for book in st.session_state.books_db:
                with st.container():
                    st.markdown(f'<div class="book-card"><h3>📖 {book["name"]}</h3></div>', unsafe_allow_html=True)
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        if st.button(f"فتح لقراءة {book['name']}", key=f"v_{book['name']}"):
                            st.toast(f"يتم الآن فتح {book['name']}...")
                    with c2:
                        if book['download'] or st.session_state.user_role == "supervisor":
                            st.download_button("📥 تحميل النسخة", data=book['data'], file_name=f"{book['name']}.pdf", key=f"d_{book['name']}")
                        else:
                            st.warning("⚠️ التحميل غير متاح (للقراءة فقط)")

    with tab2:
        st.subheader("💬 نقاشات الطلاب")
        st.chat_message("assistant").write("مرحباً بكم في منصة مقاصد الطلاب. كيف يمكننا مساعدتكم في علوم العربية اليوم؟")
        
        if msg := st.chat_input("اكتب رسالتك أو سؤالك في الإعراب..."):
            st.chat_message("user").write(msg)

    with tab3:
        st.subheader("📢 تنبيهات وتعليمات")
        st.info("سيتم رفع الملازم والكتب الخاصة بالمنهج الجديد قريباً.")
