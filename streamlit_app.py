import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

# 1. إعدادات الصفحة والتنسيق الإسلامي البراق
st.set_page_config(page_title="مَقَاصِدُ الطُلَّابِ", page_icon="🕌", layout="wide")

# الربط بمفتاح API الخاص بك (Gemini)
GENAI_API_KEY = "AIzaSyD-b_B1eHC_lWor8Q42LFZ-_N6pI6KhKNs"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Aref+Ruqaa:wght@400;700&display=swap');
    
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

    /* تنسيق الخطوط العربية */
    html, body, [class*="css"], .stText, .stMarkdown {
        font-family: 'Amiri', serif;
        text-align: right;
    }

    /* تنسيق الكروت والتبويبات */
    .stTabs [data-baseweb="tab-list"] { background-color: #1e4d2b; padding: 10px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-size: 1.2rem; }
    .custom-card {
        background: white; padding: 20px; border-radius: 15px;
        border-right: 10px solid #1e4d2b; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة مخازن البيانات (Session State)
if 'quizzes' not in st.session_state: st.session_state.quizzes = []
if 'students' not in st.session_state: st.session_state.students = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = None
if 'user' not in st.session_state: st.session_state.user = {}

CLASSES = ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الرابع العلمي", "الرابع الأدبي", "الخامس العلمي", "الخامس الأدبي", "السادس العلمي", "السادس الأدبي"]

# 3. دالة توليد الاختبار بالذكاء الاصطناعي
def generate_questions(topic, level):
    prompt = f"""
    أنت خبير تربوي. صمم اختبار اختيار من متعدد باللغة العربية عن موضوع '{topic}' لطلاب صف '{level}'.
    أريد 3 أسئلة فقط. الرد يجب أن يكون بتنسيق JSON حصراً كقائمة:
    [
      {{"q": "نص السؤال", "o": ["خيار1", "خيار2", "خيار3", "خيار4"], "a": "خيار1"}},
      ...
    ]
    """
    try:
        response = model.generate_content(prompt)
        content = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(content)
    except:
        return None

# 4. نظام تسجيل الدخول
if not st.session_state.logged_in:
    st.markdown('<div class="bright-title">مَقَاصِدُ الطُلَّابِ فِي الأدَبِ وَ الإِعْرَابِ</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        t_stu, t_sup = st.tabs(["🎓 دخول الطالب", "🔑 دخول المشرف"])
        
        with t_stu:
            with st.form("stu_login"):
                name = st.text_input("الاسم الثلاثي")
                lvl = st.selectbox("الصف الدراسي", CLASSES)
                if st.form_submit_button("دخول المنصة"):
                    if name:
                        st.session_state.logged_in, st.session_state.role = True, "student"
                        st.session_state.user = {"name": name, "class": lvl}
                        st.session_state.students.append({"الاسم": name, "الصف": lvl})
                        st.rerun()
        
        with t_sup:
            with st.form("sup_login"):
                u = st.text_input("اسم المستخدم")
                p = st.text_input("كلمة المرور", type="password")
                if st.form_submit_button("دخول"):
                    if u == "admin" and p == "12345":
                        st.session_state.logged_in, st.session_state.role = True, "supervisor"
                        st.rerun()

# 5. واجهة المشرف والطالب
else:
    st.markdown('<div class="bright-title" style="font-size: 2.5rem;">مَقَاصِدُ الطُلَّابِ</div>', unsafe_allow_html=True)
    
    if st.session_state.role == "supervisor":
        tab1, tab2, tab3 = st.tabs(["✨ صنع اختبار بالذكاء الاصطناعي", "👥 سجل الطلاب", "📊 إدارة الاختبارات"])
        
        with tab1:
            with st.form("ai_gen"):
                st.subheader("توليد اختبار فوري")
                topic = st.text_input("موضوع الدرس")
                target = st.selectbox("موجه لصف:", CLASSES)
                if st.form_submit_button("توليد ونشر الاختبار للطلاب"):
                    with st.spinner("جاري التواصل مع جيمني..."):
                        qs = generate_questions(topic, target)
                        if qs:
                            st.session_state.quizzes.append({"topic": topic, "class": target, "content": qs})
                            st.success(f"تم رفع الاختبار لطلاب {target} بنجاح!")
                        else: st.error("عذراً، فشل التوليد. حاول مرة أخرى.")
        
        with tab2:
            st.subheader("بيانات الطلاب المسجلين")
            f_class = st.selectbox("تصفية حسب الصف الدراسي:", ["الكل"] + CLASSES)
            df = pd.DataFrame(st.session_state.students)
            if not df.empty:
                if f_class != "الكل": df = df[df['الصف'] == f_class]
                st.table(df)
            else: st.info("لا يوجد طلاب مسجلون حالياً.")

    else:
        # واجهة الطالب
        st.info(f"مرحباً بك يا {st.session_state.user['name']} | الصف: {st.session_state.user['class']}")
        
        my_class_quizzes = [q for q in st.session_state.quizzes if q['class'] == st.session_state.user['class']]
        
        if not my_class_quizzes:
            st.warning("لا توجد اختبارات مخصصة لصفك حالياً.")
        else:
            for i, qz in enumerate(my_class_quizzes):
                with st.expander(f"📝 اختبار في: {qz['topic']}"):
                    correct_count = 0
                    for j, item in enumerate(qz['content']):
                        user_ans = st.radio(item['q'], item['o'], key=f"qz_{i}_{j}")
                        if user_ans == item['a']: correct_count += 1
                    
                    if st.button("تسليم النتيجة", key=f"sub_{i}"):
                        if correct_count == len(qz['content']):
                            st.balloons()
                            st.success(f"مبارك! حصلت على {correct_count} من {len(qz['content'])}")
                        else:
                            st.info(f"نتيجتك هي {correct_count} من {len(qz['content'])}")

    if st.sidebar.button("خروج من المنصة"):
        st.session_state.logged_in = False
        st.rerun()
