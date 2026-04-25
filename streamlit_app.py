import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import re

# 1. إعداد الصفحة والتنسيق
st.set_page_config(page_title="مَقَاصِدُ الطُلَّابِ", page_icon="🕌", layout="wide")

# الربط بمفتاحك الشخصي
GENAI_API_KEY = "AIzaSyD-b_B1eHC_lWor8Q42LFZ-_N6pI6KhKNs"

try:
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"خطأ في الاتصال: {e}")

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
    .stTabs [data-baseweb="tab-list"] { background-color: #1e4d2b; padding: 8px; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] { color: white !important; }
    .custom-card { background: white; padding: 20px; border-radius: 12px; border-right: 10px solid #1e4d2b; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. مخازن البيانات
if 'quizzes' not in st.session_state: st.session_state.quizzes = []
if 'students' not in st.session_state: st.session_state.students = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

CLASSES = ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الرابع العلمي", "الرابع الأدبي", "الخامس العلمي", "الخامس الأدبي", "السادس العلمي", "السادس الأدبي"]

# 3. دالة توليد وتنظيف البيانات (المطورة)
def generate_quiz_safe(topic, level):
    # تعليمات صارمة جداً للذكاء الاصطناعي
    prompt = f"""
    Act as an Arabic language expert. Create a 3-question MCQ quiz about '{topic}' for '{level}' students.
    The output MUST be a valid JSON array only. Do not include any conversational text.
    Format:
    [
      {{"q": "السؤال هنا", "o": ["خيار 1", "خيار 2", "خيار 3", "خيار 4"], "a": "خيار 1"}},
      ...
    ]
    """
    try:
        response = model.generate_content(prompt)
        raw_text = response.text
        
        # استخراج مصفوفة JSON باستخدام Regex لضمان عدم حدوث خطأ
        json_match = re.search(r'\[.*\]', raw_text, re.DOTALL)
        if json_match:
            quiz_json = json_match.group()
            return json.loads(quiz_json)
        return None
    except Exception:
        return None

# 4. تسجيل الدخول
if not st.session_state.logged_in:
    st.markdown('<div class="bright-title">مَقَاصِدُ الطُلَّابِ فِي الأدَبِ وَ الإِعْرَابِ</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        t_stu, t_sup = st.tabs(["🎓 طالب", "🔑 مشرف"])
        with t_stu:
            with st.form("s_log"):
                n, l = st.text_input("الاسم"), st.selectbox("الصف", CLASSES)
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
# 5. واجهات العمل
else:
    st.markdown('<div class="bright-title" style="font-size: 2.2rem;">مَقَاصِدُ الطُلَّابِ</div>', unsafe_allow_html=True)
    
    if st.session_state.role == "supervisor":
        tab1, tab2 = st.tabs(["✨ صنع اختبار", "👥 السجل"])
        with tab1:
            with st.form("gen"):
                topic = st.text_input("موضوع الاختبار")
                target = st.selectbox("الصف", CLASSES)
                if st.form_submit_button("نشر الاختبار فوراً"):
                    if topic:
                        with st.spinner("جاري التوليد..."):
                            data = generate_quiz_safe(topic, target)
                            if data:
                                st.session_state.quizzes.append({"topic": topic, "class": target, "content": data})
                                st.success("تم النشر!")
                            else: st.error("عذراً، لم يستجب الذكاء الاصطناعي بشكل صحيح. جرب مرة أخرى.")
        with tab2: st.table(pd.DataFrame(st.session_state.students))

    else:
        st.info(f"مرحباً {st.session_state.user['name']} | صف {st.session_state.user['class']}")
        qs = [q for q in st.session_state.quizzes if q['class'] == st.session_state.user['class']]
        if not qs: st.warning("لا توجد اختبارات")
        for qz in qs:
            with st.expander(f"📝 {qz['topic']}"):
                score = 0
                for i, item in enumerate(qz['content']):
                    ans = st.radio(item['q'], item['o'], key=f"{qz['topic']}_{i}")
                    if ans == item['a']: score += 1
                if st.button("تأكيد", key=qz['topic']):
                    st.write(f"النتيجة: {score}/{len(qz['content'])}")

    if st.sidebar.button("خروج"):
        st.session_state.logged_in = False
        st.rerun()
