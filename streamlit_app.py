import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import re

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="مَقَاصِدُ الطُلَّابِ", page_icon="🕌", layout="wide")

# 2. إعداد الاتصال بالذكاء الاصطناعي (Gemini Pro)
# تم استخدام مفتاحك الشخصي هنا مباشرة
GENAI_API_KEY = "AIzaSyD-b_B1eHC_lWor8Q42LFZ-_N6pI6KhKNs"

try:
    genai.configure(api_key=GENAI_API_KEY)
    # نستخدم gemini-pro لضمان الاستقرار التام وتجنب أخطاء 404
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"خطأ في إعداد الاتصال بـ Gemini: {e}")

# 3. التنسيق الجمالي الإسلامي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Aref+Ruqaa:wght@400;700&display=swap');
    
    /* خلفية التطبيق بنقوش عربية */
    .stApp {
        background-color: #f4f7f1;
        background-image: url("https://www.transparenttextures.com/patterns/arabesque.png");
    }

    /* العنوان البراق المتحرك */
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

    @keyframes shine { to { background-position: 200% center; } }

    /* تنسيق النصوص العربية والخطوط */
    html, body, [class*="css"], .stText, .stMarkdown {
        font-family: 'Amiri', serif;
        text-align: right;
    }

    /* تنسيق التبويبات والمكونات */
    .stTabs [data-baseweb="tab-list"] { background-color: #1e4d2b; padding: 10px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-size: 1.2rem; }
    
    .custom-card {
        background: white; padding: 25px; border-radius: 15px;
        border-right: 12px solid #1e4d2b; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* تنسيق الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #1e4d2b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. تهيئة مخازن البيانات (Session State)
if 'quizzes' not in st.session_state: st.session_state.quizzes = []
if 'students' not in st.session_state: st.session_state.students = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = None
if 'user_info' not in st.session_state: st.session_state.user_info = {}

CLASSES = ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الرابع العلمي", "الرابع الأدبي", "الخامس العلمي", "الخامس الأدبي", "السادس العلمي", "السادس الأدبي"]

# 5. وظيفة توليد الاختبار بالذكاء الاصطناعي (مع معالجة الأخطاء)
def generate_quiz_content(topic, level):
    prompt = f"""
    Create a multiple choice quiz in Arabic about '{topic}' for '{level}' students. 
    Provide exactly 3 questions. Return ONLY a valid JSON array as follows:
    [
      {{"q": "السؤال", "o": ["خيار1", "خيار2", "خيار3", "خيار4"], "a": "الإجابة الصحيحة"}}
    ]
    """
    try:
        response = model.generate_content(prompt)
        # استخدام التعبيرات النمطية لاستخراج الـ JSON فقط
        match = re.search(r'\[.*\]', response.text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except Exception:
        return None

# 6. واجهة تسجيل الدخول
if not st.session_state.logged_in:
    st.markdown('<div class="bright-title">مَقَاصِدُ الطُلَّابِ فِي الأدَبِ وَ الإِعْرَابِ</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        tab_student, tab_supervisor = st.tabs(["🎓 واجهة الطالب", "🔑 واجهة المشرف"])
        
        with tab_student:
            with st.form("stu_log"):
                n = st.text_input("الاسم الثلاثي للطالب")
                l = st.selectbox("اختر الصف الدراسي", CLASSES)
                if st.form_submit_button("دخول المنصة"):
                    if n:
                        st.session_state.logged_in = True
                        st.session_state.role = "student"
                        st.session_state.user_info = {"الاسم": n, "الصف": l}
                        st.session_state.students.append({"الاسم": n, "الصف": l})
                        st.rerun()
                    else: st.error("يرجى كتابة الاسم")
                    
        with tab_supervisor:
            with st.form("sup_log"):
                u = st.text_input("اسم المستخدم")
                p = st.text_input("كلمة المرور", type="password")
                if st.form_submit_button("دخول"):
                    if u == "admin" and p == "12345":
                        st.session_state.logged_in = True
                        st.session_state.role = "supervisor"
                        st.rerun()
                    else: st.error("بيانات المشرف غير صحيحة")

# 7. واجهة العمل بعد الدخول
else:
    st.markdown('<div class="bright-title" style="font-size: 2.5rem;">مَقَاصِدُ الطُلَّابِ</div>', unsafe_allow_html=True)
    
    # واجهة المشرف
    if st.session_state.role == "supervisor":
        tab1, tab2 = st.tabs(["✨ صنع اختبار ذكي (Gemini)", "👥 سجل الطلاب المسجلين"])
        
        with tab1:
            st.subheader("توليد اختبار فوري بالذكاء الاصطناعي")
            with st.form("ai_form"):
                topic = st.text_input("ما هو موضوع الاختبار؟ (مثال: كان وأخواتها، العصر العباسي)")
                level = st.selectbox("حدد الصف المستهدف", CLASSES)
                if st.form_submit_button("توليد ونشر الاختبار"):
                    if topic:
                        with st.spinner("جاري التواصل مع جيمني برو لتوليد الأسئلة..."):
                            quiz_data = generate_quiz_content(topic, level)
                            if quiz_data:
                                st.session_state.quizzes.append({"topic": topic, "class": level, "content": quiz_data})
                                st.success(f"تم بنجاح رفع الاختبار لطلاب {level}!")
                            else: st.error("عذراً، حدث خطأ في معالجة البيانات من الذكاء الاصطناعي. حاول مرة أخرى.")
                    else: st.warning("يرجى إدخال الموضوع")

        with tab2:
            st.subheader("قائمة الطلاب المتواجدين حالياً")
            if st.session_state.students:
                st.table(pd.DataFrame(st.session_state.students))
            else: st.info("لا يوجد طلاب مسجلون حالياً.")

    # واجهة الطالب
    else:
        st.info(f"مرحباً بك يا {st.session_state.user_info['الاسم']} | الصف: {st.session_state.user_info['الصف']}")
        
        # عرض الاختبارات الخاصة بصف الطالب فقط
        class_quizzes = [q for q in st.session_state.quizzes if q['class'] == st.session_state.user_info['الصف']]
        
        if not class_quizzes:
            st.warning("لا توجد اختبارات متاحة لصفك الدراسي في الوقت الحالي.")
        else:
            for idx, qz in enumerate(class_quizzes):
                with st.container():
                    st.markdown(f'<div class="custom-card"><h3>📝 اختبار: {qz["topic"]}</h3></div>', unsafe_allow_html=True)
                    score = 0
                    for i, item in enumerate(qz['content']):
                        ans = st.radio(f"{i+1}. {item['q']}", item['o'], key=f"q_{idx}_{i}")
                        if ans == item['a']: score += 1
                    
                    if st.button(f"تأكيد إجابة اختبار {qz['topic']}", key=f"btn_{idx}"):
                        if score == len(qz['content']):
                            st.balloons()
                            st.success(f"أحسنت صنعاً! درجتك هي: {score} من {len(qz['content'])}")
                        else:
                            st.info(f"نتيجتك في هذا الاختبار هي: {score} من {len(qz['content'])}")

    # خيار تسجيل الخروج في القائمة الجانبية
    if st.sidebar.button("خروج من المنصة"):
        st.session_state.logged_in = False
        st.rerun()
