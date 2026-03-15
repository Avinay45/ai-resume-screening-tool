import streamlit as st
import tempfile
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from nlp.resume_parser import parse_resume
from rag.rag_pipeline import RAGPipeline
from utils.llm_evaluator import evaluate_candidate
from utils.report_generator import generate_report
from utils.resume_chatbot import ask_resume_chatbot

st.set_page_config(page_title="AI Resume Screening Tool", layout="wide")

st.title("🤖 AI Resume Screening Dashboard")

# Session state initialization
if "ranking_data" not in st.session_state:
    st.session_state.ranking_data = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

job_description = st.text_area(
    "Enter Job Description",
    height=200
)

if st.button("Analyze Candidates"):

    if not uploaded_files or not job_description:
        st.warning("Please upload resumes and enter a job description.")
        st.stop()

    resumes = []

    for uploaded_file in uploaded_files:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        resume_text = parse_resume(tmp_path)

        resumes.append((uploaded_file.name, resume_text))

        os.remove(tmp_path)

    rag = RAGPipeline()
    rag.index_resumes(resumes)

    results = rag.retrieve_candidates(job_description)

    ranking_data = []

    for file_name, resume_text in results:

        evaluation = evaluate_candidate(resume_text, job_description)

        score = 0

        for line in evaluation.split("\n"):
            if "Candidate Score" in line:
                try:
                    score = int(line.split(":")[1].strip())
                except:
                    score = 0

        ranking_data.append({
            "Candidate": file_name,
            "Score": score,
            "Evaluation": evaluation
        })

    st.session_state.ranking_data = ranking_data


ranking_data = st.session_state.ranking_data

col1, col2 = st.columns([3,1])


# LEFT SIDE DASHBOARD
with col1:

    if ranking_data:

        df = pd.DataFrame(ranking_data)
        df = df.sort_values(by="Score", ascending=False)

        st.subheader("🏆 Candidate Leaderboard")

        st.dataframe(df[["Candidate","Score"]], use_container_width=True)

        top_candidate = df.iloc[0]

        st.success(
            f"🏆 Top Candidate: {top_candidate['Candidate']} — Score: {top_candidate['Score']}"
        )

        st.subheader("📊 Candidate Ranking Chart")

        fig = px.bar(
            df,
            x="Candidate",
            y="Score",
            color="Score",
            color_continuous_scale="blues"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📄 Candidate Analysis")

        for i,row in enumerate(ranking_data):

            st.markdown(f"### {row['Candidate']}")

            st.progress(row["Score"]/100)

            st.text(row["Evaluation"])

            matching=[]
            missing=[]
            section=None

            for line in row["Evaluation"].split("\n"):

                if "Matching Skills" in line:
                    section="matching"

                elif "Missing Skills" in line:
                    section="missing"

                elif "-" in line:

                    skill=line.replace("-","").strip()

                    if section=="matching":
                        matching.append(skill)

                    elif section=="missing":
                        missing.append(skill)

            labels=["Matching Skills","Missing Skills"]
            values=[len(matching),len(missing)]

            pie_fig=go.Figure(
                data=[go.Pie(labels=labels,values=values)]
            )

            st.plotly_chart(pie_fig,use_container_width=True)

            report_file=generate_report(
                row["Candidate"],
                row["Score"],
                row["Evaluation"]
            )

            with open(report_file,"rb") as f:

                st.download_button(
                    label="📄 Download Recruiter Report",
                    data=f,
                    file_name=report_file,
                    mime="application/pdf",
                    key=f"download_{i}"
                )

            st.divider()


# RIGHT SIDE CHATBOT
with col2:

    st.subheader("💬 AI Resume Chatbot")

    if ranking_data:

        # Display chat history
        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):
                st.write(message["content"])

        prompt = st.chat_input("Ask about the candidates")

        if prompt:

            st.session_state.chat_history.append(
                {"role":"user","content":prompt}
            )

            with st.chat_message("user"):
                st.write(prompt)

            resume_context=""

            for row in ranking_data:

                resume_context+=f"\nCandidate: {row['Candidate']}\n"
                resume_context+=row["Evaluation"]+"\n"

            answer = ask_resume_chatbot(prompt,resume_context)

            with st.chat_message("assistant"):
                st.write(answer)

            st.session_state.chat_history.append(
                {"role":"assistant","content":answer}
            )

    else:

        st.info("Analyze candidates first to enable chatbot.")