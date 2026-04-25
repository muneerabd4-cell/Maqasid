import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="مَقَاصِدُ الطُلَّابِ", page_icon="🕌", layout="wide")

# الربط بمفتاحك الخاص
GENAI_API_KEY = "AIzaSyD-b_B1eHC_lWor8Q42LFZ-_N6pI6KhKNs"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. التنسيق الجمالي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Aref+Ruqaa:wght@400;700&display=swap');
    .stApp { background-color: #f4f7f1; background-image: url("https://www.transparenttextures.com/patterns/arabesque.png"); }
    html, body, [class*="css"] { font-family: 'Amiri', serif; text-align: right; }
    .bright-title {
        font-family: 'Aref Ruqaa', serif; font-size: 3rem; font-weight: bold; text-align: center;
        background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
        background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite; padding: 15px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .custom-card { background: white; padding: 20px; border-radius: 15px; border-right: 10px solid #1e4d2b; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1e4d2b; padding: 10px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات
if 'quizzes' not in st.session_state: st.session_state.quizzes = []
if 'students' not in st.session_state: st.session_state.students = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

CLASSES = ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الرابع العلمي", "الرابع الأدبي", "الخامس العلمي", "الخامس الأدبي", "السادس العلمي", "السادس الأدبي"]

# 4. دالة استخراج الـ JSON الذكية (لحل مشكلة الخطأ)
def safe_generate_quiz(topic, level):
    prompt = f"صمم اختبار MCQs بالعربية عن {topic} لصف {level}. 3 أسئلة فقط. الرد يجب أن يكون بصيغة JSON فقط كقائمة: [{{'q': '..', 'o': ['..','..','..','..'], 'a': '..'}}]"
    try:
        response = model.generate_content(prompt)
        text = response.text
        # استخراج مابين الأقواس المربعة لضمان صحة الـ JSON
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except Exception as e:
        st.error(f"خطأ تقني: {e}")
        return None

# 5. تسجيل الدخول
if not st.session_state.logged_in:
    st.markdown('<div class="bright-title">مَقَاصِدُ الطُلَّابِ فِي الأدَبِ وَ الإِعْرَابِ</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        t_stu, t_sup = st.tabs(["🎓 طالب", "🔑 مشرف"])
        with t_stu:
            with st.form("s_log"):
                n = st.text_input("الاسم")
                l = st.selectbox("الصف", CLASSES)
                if st.form_submit_button("دخول"):
                    if n:
                        st.session_state.logged_in, st.session_state.role = True, "student"
                        st.session_state.user = {"name": n, "class": l}
                        st.session_state.students.append({"الاسم": n, "الصف": l})
                        st.rerun()
        with t_sup:
            with st.form("p_log"):
                u, p = st.text_input("اليوزر"), st.text_input("الباسورد", type="password")
                if st.form_submit_button("دخول"):
                    if u == "admin" and p == "12345":
                        st.session_state.logged_in, st.session_state.role = True, "supervisor"
                        st.rerun()

# 6. الواجهة بعد الدخول
else:
    st.markdown('<div class="bright-title" style="font-size: 2.2rem;">مَقَاصِدُ الطُلَّابِ</div>', unsafe_allow_html=True)
    
    if st.session_state.role == "supervisor":
        tab1, tab2 = st.tabs(["✨ صنع اختبار ذكي", "👥 سجل الطلاب"])
        with tab1:
            with st.form("gen_quiz"):
                topic = st.text_input("موضوع الاختبار")
                target = st.selectbox("الصف المستهدف", CLASSES)
                if st.form_submit_button("توليد ونشر الاختبار"):
                    if topic:
                        with st.spinner("جاري التوليد..."):
                            qs = safe_generate_quiz(topic, target)
                            if qs:
                                st.session_state.quizzes.append({"topic": topic, "class": target, "content": qs})
                                st.success("تم النشر بنجاح!")
                            else: st.error("فشل التوليد، حاول مرة أخرى.")
        with tab2:
            st.table(pd.DataFrame(st.session_state.students))

    else:
        st.info(f"الطالب: {st.session_state.user['name']} | الصف: {st.session_state.user['class']}")
        my_quizzes = [q for q in st.session_state.quizzes if q['class'] == st.session_state.user['class']]
        if not my_quizzes: st.warning("لا توجد اختبارات لصفك")
        for qz in my_quizzes:
            with st.expander(f"📝 اختبار: {qz['topic']}"):
                score = 0
                for item in qz['content']:
                    ans = st.radio(item['q'], item['o'], key=item['q'])
                    if ans == item['a']: score += 1
                if st.button("النتيجة", key=qz['topic']):
                    st.write(f"درجتك: {score}/{len(qz['content'])}")

    if st.sidebar.button("خروج"):
        st.session_state.logged_in = False
        st.rerun()
