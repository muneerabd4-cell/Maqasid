import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

# 1. إعدادات الصفحة والتصميم الإسلامي
st.set_page_config(page_title="منصة مَقَاصِدُ الطُلَّابِ", layout="wide")

# استبدل 'YOUR_API_KEY' بمفتاح Gemini الخاص بك
GENAI_API_KEY = "YOUR_API_KEY" 
genai.configure(api_key=GENAI_API_KEY)

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
    .quiz-card { background: white; padding: 20px; border-radius: 15px; border-right: 10px solid #1e4d2b; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1e4d2b; padding: 10px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة البيانات
if 'quizzes' not in st.session_state: st.session_state.quizzes = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'user_info' not in st.session_state: st.session_state.user_info = {}

CLASSES = ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الرابع العلمي", "الرابع الأدبي", "الخامس العلمي", "الخامس الأدبي", "السادس العلمي", "السادس الأدبي"]

# 3. وظيفة توليد الاختبار بالذكاء الاصطناعي
def generate_quiz_ai(topic, class_level):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    قم بإنشاء اختبار اختيار من متعدد باللغة العربية حول موضوع: {topic} لطلاب الصف: {class_level}.
    أريد 3 أسئلة فقط. لكل سؤال 4 خيارات.
    يجب أن يكون الرد بصيغة JSON حصراً كالتالي:
    [
      {{"question": "السؤال الأول", "options": ["خيار 1", "خيار 2", "خيار 3", "خيار 4"], "answer": "خيار 1"}},
      ...
    ]
    """
    try:
        response = model.generate_content(prompt)
        # تنظيف النص المستلم من أي علامات Markdown
        json_str = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(json_str)
    except Exception as e:
        st.error(f"حدث خطأ في الاتصال بالذكاء الاصطناعي: {e}")
        return None

# 4. واجهة تسجيل الدخول
if not st.session_state.logged_in:
    st.markdown('<div class="bright-title">مَقَاصِدُ الطُلَّابِ فِي الأدَبِ وَ الإِعْرَابِ</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        t_stu, t_sup = st.tabs(["🎓 دخول الطالب", "🔑 دخول المشرف"])
        with t_stu:
            with st.form("stu_log"):
                n = st.text_input("الاسم الثلاثي")
                l = st.selectbox("الصف الدراسي", CLASSES)
                if st.form_submit_button("دخول"):
                    if n:
                        st.session_state.logged_in, st.session_state.user_role = True, "student"
                        st.session_state.user_info = {"الاسم": n, "الصف": l}
                        st.rerun()
        with t_sup:
            with st.form("sup_log"):
                u, p = st.text_input("المشرف"), st.text_input("كلمة المرور", type="password")
                if st.form_submit_button("دخول"):
                    if u == "admin" and p == "12345":
                        st.session_state.logged_in, st.session_state.user_role = True, "supervisor"
                        st.rerun()

# 5. الواجهة الرئيسية
else:
    st.markdown('<div class="bright-title">مَقَاصِدُ الطُلَّابِ</div>', unsafe_allow_html=True)
    
    if st.session_state.user_role == "supervisor":
        tab1, tab2 = st.tabs(["📝 صناعة الاختبار بالذكاء الاصطناعي", "📊 الاختبارات المنشورة"])
        
        with tab1:
            st.subheader("توليد اختبار ذكي")
            col_a, col_b = st.columns(2)
            with col_a:
                topic = st.text_input("موضوع الاختبار (مثلاً: الفاعل، المتنبي، العصر الجاهلي)")
            with col_b:
                target_class = st.selectbox("الفئة المستهدفة", CLASSES)
            
            if st.button("توليد الأسئلة بواسطة Gemini ✨"):
                if topic:
                    with st.spinner("جاري تفكير الذكاء الاصطناعي..."):
                        questions = generate_quiz_ai(topic, target_class)
                        if questions:
                            st.session_state.temp_quiz = {"topic": topic, "class": target_class, "questions": questions}
                            st.success("تم توليد الأسئلة بنجاح! راجعها بالأسفل ثم انشرها.")
                else: st.warning("يرجى كتابة موضوع أولاً")

            if 'temp_quiz' in st.session_state:
                st.markdown("---")
                st.info(f"معاينة اختبار: {st.session_state.temp_quiz['topic']} لصف {st.session_state.temp_quiz['class']}")
                for i, q in enumerate(st.session_state.temp_quiz['questions']):
                    st.write(f"**س{i+1}: {q['question']}**")
                
                if st.button("✅ رفع ونشر الاختبار للطلاب"):
                    st.session_state.quizzes.append(st.session_state.temp_quiz)
                    del st.session_state.temp_quiz
                    st.success("تم رفع الاختبار بتبويب الطلاب!")
        
        with tab2:
            if not st.session_state.quizzes: st.write("لا توجد اختبارات منشورة بعد.")
            for quiz in st.session_state.quizzes:
                st.markdown(f"<div class='quiz-card'><b>الموضوع:</b> {quiz['topic']} | <b>الصف:</b> {quiz['class']}</div>", unsafe_allow_html=True)

    else:
        # واجهة الطالب
        st.subheader(f"أهلاً بك يا {st.session_state.user_info['الاسم']} | صف {st.session_state.user_info['الصف']}")
        tab_quiz = st.tabs(["📝 اختبارات صفي"])
        
        with tab_quiz[0]:
            # تصفية الاختبارات لتظهر حسب مرحلة الطالب فقط
            my_quizzes = [q for q in st.session_state.quizzes if q['class'] == st.session_state.user_info['الصف']]
            
            if not my_quizzes:
                st.info("لا توجد اختبارات متاحة لصفك حالياً.")
            else:
                for quiz in my_quizzes:
                    with st.expander(f"📖 اختبار في: {quiz['topic']}"):
                        score = 0
                        for i, q in enumerate(quiz['questions']):
                            answer = st.radio(q['question'], q['options'], key=f"q_{quiz['topic']}_{i}")
                            if answer == q['answer']: score += 1
                        
                        if st.button("تسليم الإجابة", key=f"btn_{quiz['topic']}"):
                            if score == len(quiz['questions']):
                                st.balloons()
                                st.success(f"أحسنت! درجتك كاملة: {score}/{len(quiz['questions'])}")
                            else:
                                st.warning(f"درجتك هي: {score}/{len(quiz['questions'])}")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
