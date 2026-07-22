import streamlit as st
import re

from services.interview_service import InterviewService
from services.transcript_service import TranscriptService

def initialize_services():
    if "interview_service" not in st.session_state:
        st.session_state.interview_service = InterviewService()
    if "transcript_service" not in st.session_state:
        st.session_state.transcript_service = TranscriptService()

def initialize_session_state():
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    if "interview_completed" not in st.session_state:
        st.session_state.interview_completed = False
    if "evaluation_result" not in st.session_state:
        st.session_state.evaluation_result = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"

def load_css():
    st.markdown("""
    <style>
    /* 1. Global Reset & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #0F172A !important;
        color: #FFFFFF !important;
    }
    .stApp { background-color: #0F172A !important; }

    /* 2. Hide Default Streamlit Chrome */
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    .element-container p { margin-bottom: 0 !important; }

    /* 3. Main Dashboard Layout Container (SAFE) */
    .block-container {
        max-width: 1500px !important;
        padding-top: 120px !important; 
    }

    /* 4. Top Sticky Navigation Bar */
    .top-nav {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background-color: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 60px;
        z-index: 999999;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .nav-logo { font-size: 24px; font-weight: 800; color: white; letter-spacing: -0.5px; }
    .nav-step { font-size: 15px; font-weight: 600; color: #CBD5E1; background: #1E293B; padding: 10px 24px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.05); }

    /* 5. Premium Glass Cards (Native Streamlit Border Wrappers) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1E293B !important;
        border-radius: 24px !important;
        padding: 32px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
        border: none !important;
    }

    /* 6. Input Styling */
    .stTextInput input, .stTextArea textarea {
        height: 56px !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        padding-left: 18px !important;
        padding-right: 18px !important;
        width: 100% !important;
        background-color: #0F172A !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        transition: all 0.3s ease;
    }
    .stTextArea textarea {
        height: 220px !important;
        padding-top: 18px !important;
        line-height: 1.6 !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25) !important;
    }
    .stTextInput label p {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #FFFFFF !important;
        margin-bottom: 12px !important;
    }
    .stTextInput {
        margin-bottom: 24px !important;
    }

    /* 7. Button Styling */
    .stButton button {
        height: 56px !important;
        border-radius: 12px !important;
        width: 100% !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6, #8B5CF6) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
    }
    button[kind="secondary"] {
        background: #1E293B !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    button[kind="secondary"]:hover {
        background: #334155 !important;
    }

    /* 8. Landing Page Flexbox Centering (UNTOUCHED) */
    [data-testid="stVerticalBlock"]:has(.landing-page-marker) {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        height: 80vh !important;
        width: 100% !important;
    }
    [data-testid="stVerticalBlock"]:has(.landing-page-marker) > .element-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }
    .landing-title { font-size: 56px !important; font-weight: 800 !important; color: white !important; margin: 0 0 16px 0 !important; letter-spacing: -1px !important; text-align: center !important; }
    .landing-subtitle { font-size: 20px !important; color: #94A3B8 !important; max-width: 600px !important; line-height: 1.6 !important; margin: 0 0 40px 0 !important; text-align: center !important; }
    
    [data-testid="stVerticalBlock"]:has(.landing-page-marker) .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    [data-testid="stVerticalBlock"]:has(.landing-page-marker) .stButton button {
        width: 280px !important;
        height: 56px !important;
        margin: 0 !important;
    }

    /* 9. Metric Row Grid */
    .metric-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 24px;
        margin-bottom: 32px;
    }
    .metric-card {
        background-color: #1E293B;
        border-radius: 24px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .metric-label { font-size: 15px; font-weight: 600; color: #94A3B8; text-transform: uppercase; margin-bottom: 16px; letter-spacing: 0.5px; }
    .metric-value { font-size: 38px; font-weight: 800; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .metric-value.text-md { font-size: 28px; }

    /* 10. Typography Classes */
    .q-title { font-size: 24px; font-weight: 700; color: white; margin-bottom: 16px; }
    .q-text { font-size: 16px; color: #94A3B8; margin-bottom: 24px; line-height: 1.6; }
    .eval-title { font-size: 24px; font-weight: 700; color: white; margin-bottom: 20px; }
    .eval-text { font-size: 16px; color: #CBD5E1; line-height: 1.6; margin-bottom: 12px; }
    .page-title { font-size: 42px; font-weight: 800; color: white; margin-bottom: 32px; letter-spacing: -0.5px; }
    
    /* 11. Welcome Card Content Centering */
    .welcome-card-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        height: 196px; /* 196 + 32 + 32 padding = exactly 260px height */
    }
    </style>
    """, unsafe_allow_html=True)

def render_top_nav(step: str):
    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-logo">🤖 AI Interview</div>
        <div class="nav-step">{step}</div>
    </div>
    """, unsafe_allow_html=True)

def start_interview(role: str, skills: str, experience: str):
    if not role or not skills or not experience:
        st.error("Please fill in Role, Skills, and Experience.")
        return

    try:
        with st.spinner("Generating interview questions..."):
            questions = st.session_state.interview_service.start_interview(
                role=role,
                skills=skills,
                experience=experience
            )
            
            st.session_state.questions = questions
            st.session_state.interview_started = True
            st.session_state.interview_completed = False
            st.session_state.evaluation_result = None
            
            for i in range(len(questions)):
                key = f"answer_input_{i}"
                if key in st.session_state:
                    del st.session_state[key]
            
    except Exception as e:
        st.error(f"Failed to start interview: {e}")

def submit_interview():
    answers_list = []
    for i in range(len(st.session_state.questions)):
        key = f"answer_input_{i}"
        ans = st.session_state.get(key, "").strip()
        if not ans:
            st.error(f"Please answer Question {i+1}.")
            return
        answers_list.append(ans)

    try:
        with st.spinner("Evaluating your answers..."):
            st.session_state.answers = answers_list
            result = st.session_state.interview_service.evaluate_interview(
                role=st.session_state.role,
                skills=st.session_state.skills,
                experience=st.session_state.experience,
                questions=st.session_state.questions,
                answers=answers_list
            )
            
            st.session_state.evaluation_result = result
            st.session_state.interview_completed = True
            
    except Exception as e:
        st.error(f"Evaluation failed: {e}")
        return

    st.rerun()

def save_interview():
    try:
        data = st.session_state.evaluation_result
        if not data:
            st.error("No evaluation to save.")
            return

        transcript_data = {
            "role": st.session_state.role,
            "skills": st.session_state.skills,
            "experience": st.session_state.experience,
            "evaluation_result": data
        }

        path = st.session_state.transcript_service.save_interview(transcript_data)
        st.success(f"Interview saved to: {path}")
    except Exception as e:
        st.error(f"Failed to save interview: {e}")

def main():
    st.set_page_config(page_title="AI Interview Agent", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")
    load_css()
    initialize_services()
    initialize_session_state()

    # PAGE 1: Landing Page
    if st.session_state.current_page == "landing":
        render_top_nav("Welcome")
        
        with st.container():
            st.markdown('<span class="landing-page-marker"></span>', unsafe_allow_html=True)
            st.markdown("<div class='landing-title'>🤖 Your AI Interview</div>", unsafe_allow_html=True)
            st.markdown("<div class='landing-subtitle'>Practice AI-powered technical interviews and receive instant feedback.</div>", unsafe_allow_html=True)
            
            if st.button(" Start AI Interview", type="primary"):
                st.session_state.current_page = "dashboard"
                st.rerun()
        return

    # Determine Top Nav Step
    if st.session_state.interview_completed:
        nav_step = "Evaluation"
    elif st.session_state.interview_started:
        nav_step = "Interview"
    else:
        nav_step = "Dashboard"
        
    render_top_nav(nav_step)

    # PAGE 2, 3, 4: Dashboard Layout - NATIVE STREAMLIT STRUCTURE
    left_col, right_col = st.columns([3, 7], gap="large")

    with left_col:
        with st.container(border=True):
            st.markdown("<div style='font-size: 24px; font-weight: 700; color: white; margin-bottom: 32px;'>👤 Candidate Profile</div>", unsafe_allow_html=True)
            
            role = st.text_input("Role", placeholder="e.g. Full Stack Developer", value=st.session_state.get("role", ""))
            skills = st.text_input("Skills", placeholder="e.g. Python, React, AWS", value=st.session_state.get("skills", ""))
            experience = st.text_input("Experience", placeholder="e.g. 3 years", value=st.session_state.get("experience", ""))
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Start Interview", type="primary"):
                st.session_state.role = role
                st.session_state.skills = skills
                st.session_state.experience = experience
                start_interview(role, skills, experience)

    with right_col:
        
        if st.session_state.interview_completed and st.session_state.evaluation_result:
            result = st.session_state.evaluation_result
            evaluations = result.get("evaluations", [])
            
            scores = []
            for e in evaluations:
                s = str(e.get("score", ""))
                match = re.search(r'\d+', s)
                if match:
                    scores.append(int(match.group()))
            
            avg_score = sum(scores) / len(scores) if scores else 0
            tech_rating = "Excellent" if avg_score >= 8 else "Good" if avg_score >= 6 else "Needs Work"
            comm_rating = "Clear" if avg_score >= 7 else "Improvement Needed"
            recommendation = "Advance" if avg_score >= 7.5 else "Keep Practicing"
            
            def get_val_class(val):
                if len(val) > 13: return "text-md"
                return ""

            st.markdown("<div class='page-title'>📊 Evaluation Results</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card">
                    <div class="metric-label">Overall Score</div>
                    <div class="metric-value">{avg_score:.1f}/10</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Technical Rating</div>
                    <div class="metric-value {get_val_class(tech_rating)}">{tech_rating}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Communication</div>
                    <div class="metric-value {get_val_class(comm_rating)}">{comm_rating}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Recommendation</div>
                    <div class="metric-value {get_val_class(recommendation)}">{recommendation}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            all_strengths = []
            all_weaknesses = []
            all_missing = []
            for e in evaluations:
                all_strengths.extend(e.get("strengths", []))
                all_weaknesses.extend(e.get("weaknesses", []))
                all_missing.extend(e.get("missing_concepts", []))
                
            def dedupe(seq):
                seen = set()
                return [x for x in seq if not (x in seen or seen.add(x))]

            all_strengths = dedupe(all_strengths)
            all_weaknesses = dedupe(all_weaknesses)
            all_missing = dedupe(all_missing)

            with st.container(border=True):
                st.markdown('<div class="eval-title">📋 Executive Summary</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="eval-text">{result.get("final_report", "")}</div>', unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown('<div class="eval-title">⭐ Strengths</div>', unsafe_allow_html=True)
                if all_strengths:
                    html = "".join([f"<li class='eval-text' style='margin-bottom:12px;'>{s}</li>" for s in all_strengths])
                    st.markdown(f"<ul style='padding-left:20px;'>{html}</ul>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='eval-text'>No notable strengths found.</div>", unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown('<div class="eval-title">❌ Weaknesses</div>', unsafe_allow_html=True)
                if all_weaknesses:
                    html = "".join([f"<li class='eval-text' style='margin-bottom:12px;'>{w}</li>" for w in all_weaknesses])
                    st.markdown(f"<ul style='padding-left:20px;'>{html}</ul>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='eval-text'>No notable weaknesses found.</div>", unsafe_allow_html=True)
                    
            with st.container(border=True):
                st.markdown('<div class="eval-title">📚 Learning Roadmap</div>', unsafe_allow_html=True)
                if all_missing:
                    html = "".join([f"<li class='eval-text' style='margin-bottom:12px;'>{m}</li>" for m in all_missing])
                    st.markdown(f"<ul style='padding-left:20px;'>{html}</ul>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='eval-text'>You are well versed in these topics.</div>", unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown('<div class="eval-title">🎯 Final Recommendation</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="eval-text" style="font-size: 24px; font-weight: 700; color: #8B5CF6;">{recommendation}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="eval-text">Based on your overall score of {avg_score:.1f}/10.</div>', unsafe_allow_html=True)

            st.markdown("<div class='page-title' style='margin-top: 48px; font-size: 32px;'>🔍 Detailed Feedback</div>", unsafe_allow_html=True)
            for i, (q, a, e) in enumerate(zip(result.get("questions", []), result.get("answers", []), evaluations), 1):
                with st.container(border=True):
                    st.markdown(f'<div class="eval-title">Question {i}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="eval-text"><strong>Q:</strong> {q}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="eval-text"><strong>Your Answer:</strong> {a}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="eval-text"><strong>Score:</strong> {e.get("score", "N/A")}/10</div>', unsafe_allow_html=True)
                    ideal = e.get("ideal_answer")
                    if ideal:
                        st.markdown(f'<div class="eval-text" style="color: #22C55E; margin-top: 16px;"><strong>✅ Ideal Answer:</strong> {ideal}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2, gap="large")
            with col_a:
                if st.button("💾 Save Interview", type="primary"):
                    save_interview()
            with col_b:
                if st.button("🔄 Start New Interview", type="secondary"):
                    keys = ["questions", "answers", "evaluation_result", "interview_started", "interview_completed", "role", "skills", "experience"]
                    for key in keys: st.session_state.pop(key, None)
                    st.session_state.current_page = "dashboard"
                    st.rerun()

        elif st.session_state.interview_started:
            st.markdown("<div class='page-title'>🤖 Interview Questions</div>", unsafe_allow_html=True)
            st.markdown("<div class='eval-text' style='margin-bottom: 32px;'>Please provide detailed answers for the best evaluation.</div>", unsafe_allow_html=True)
            
            for i, question in enumerate(st.session_state.questions):
                with st.container(border=True):
                    st.markdown(f'<div class="q-title">Question {i+1}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="q-text">{question}</div>', unsafe_allow_html=True)
                    
                    st.text_area(
                        "Your Answer",
                        key=f"answer_input_{i}",
                        label_visibility="collapsed",
                        placeholder="Type your detailed answer here...",
                        height=220
                    )
                
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Submit Interview", type="primary"):
                submit_interview()
                
        else:
            with st.container(border=True):
                st.markdown("""
                <div class="welcome-card-content">
                    <div style="font-size: 64px; margin-bottom: 16px;">Welcome to your dashboard</div>
                    <div style="font-size: 42px; font-weight: 800; color: white; margin-bottom: 16px;"></div>
                    <div style="font-size: 20px; color: #94A3B8;">Fill your Candidate Profile on the left and click <b>Start Interview</b> to begin.</div>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
