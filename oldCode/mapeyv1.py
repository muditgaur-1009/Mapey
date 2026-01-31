import os
import tempfile
import streamlit as st
from typing import TypedDict, List

import faiss
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool

from langgraph.graph import StateGraph, END

from tavily import TavilyClient


# ======================================================
# CONFIG
# ======================================================

st.set_page_config(page_title="Mapey v3", layout="wide")

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
llm = OllamaLLM(model="llama3.2:1b", temperature=0.4,num_ctx=1048)
parser = StrOutputParser()

tavily = TavilyClient(api_key="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")


# ======================================================
# VECTOR STORE (FAISS)
# ======================================================

class VectorStore:
    def __init__(self):
        self.index = None
        self.texts = []

    def add_texts(self, texts: List[str]):
        if not texts:
            return
        embeds = EMBED_MODEL.encode(texts)
        dim = embeds.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeds)
        self.texts.extend(texts)

    def search(self, query: str, k=4):
        if self.index is None:
            return []
        q_emb = EMBED_MODEL.encode([query])
        D, I = self.index.search(q_emb, k)
        return [self.texts[i] for i in I[0]]


VECTOR_DB = VectorStore()


# ======================================================
# UTILS
# ======================================================

def read_resume_file(uploaded_file) -> str:
    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        return uploaded_file.read().decode("utf-8", errors="ignore")


def chunk_text(text, size=500):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]


# ======================================================
# WEB SEARCH TOOL
# ======================================================

@tool
def web_search(query: str) -> str:
    """Search the web for learning resources."""
    res = tavily.search(query=query, max_results=5)
    return "\n".join(r["url"] for r in res["results"])


# ======================================================
# STATE
# ======================================================

class MapeyState(TypedDict):
    topic: str
    resume: str
    jd: str
    analysis: str
    skill_gaps: str
    curriculum: str
    rag_context: str
    resources: str
    roadmap: str


# ======================================================
# AGENTS
# ======================================================

# ---- Topic Analyzer ----
def topic_analyzer(state: MapeyState):

    prompt = PromptTemplate.from_template("""
You are a senior industry expert, hiring manager, and career mentor.

Your task is to deeply analyze a target career role and produce a
practical, execution-ready skill strategy for a candidate.

Target Role:
{topic}
Provide a structured expert analysis with the following sections:

1. Role Breakdown
   - What this role actually does day-to-day
   - Key problem types handled

2. Core Skill Domains
   - Technical skills (grouped by category)
   - Foundational theory
   - Tooling & platforms
   - Soft & meta-skills

3. Industry Expectations (2024–2026)
   - What hiring managers really look for
   - Typical interview focus areas
   - Signals of strong vs weak candidates

4. Learning & Mastery Order
   - Phase 1: Foundations (what to learn first)
   - Phase 2: Applied skills
   - Phase 3: Advanced / specialization

5. Portfolio & Proof Strategy
   - Project types that strongly signal competence
   - What makes projects stand out

6. Common Pitfalls
   - What most learners waste time on
   - Skills that are overhyped but low ROI

7. Career Path Progression
   - Entry-level expectations
   - Mid-level expectations
   - Long-term growth paths

Write concisely but with high signal.
Avoid generic advice. Be specific and practical.
""")

    chain = prompt | llm | parser
    return {"analysis": chain.invoke({"topic": state["topic"]})}


# ---- Skill Gap Agent ----

def skill_gap_agent(state: MapeyState):

    prompt = PromptTemplate.from_template("""
You are an expert technical recruiter and career coach.

Your job is to perform a deep skill-gap analysis by comparing:
1) The user's resume
2) The target job description
3) The target role expectations

Target Role:
{topic}

Resume:
{resume}

Job Description:
{jd}

Perform structured analysis with these sections:

1. Verified Strengths
   - Skills clearly demonstrated with evidence
   - Practical experience vs theoretical exposure

2. Partial Matches
   - Skills mentioned but lacking depth or projects
   - What level is missing (beginner / intermediate / advanced)

3. Critical Missing Skills
   - Must-have skills from JD not found in resume
   - Foundational gaps that block progress

4. Priority Gap Ranking
   Rank gaps by:
   - Hiring impact
   - Learning difficulty
   - Dependency order

   Provide: High / Medium / Low priority

5. Interview Risk Areas
   - Topics likely to fail interviews
   - Concepts that need strong clarity

6. Actionable Learning Targets
   Convert gaps into:
   - Specific topics to study
   - Tooling to practice
   - Project types to build

7. Readiness Score
   Estimate:
   - Resume vs JD match percentage
   - Resume vs ideal role percentage

Be honest, specific, and practical.
Avoid generic statements.
""")

    chain = prompt | llm | parser

    result = chain.invoke({
        "topic": state["topic"],
        "resume": state["resume"],
        "jd": state["jd"]
    })

    return {
        "skill_gaps": result
    }


# ---- RAG Retriever ----
def rag_retriever(state: MapeyState):

    query = f"Learning resources for {state['topic']} skills"
    chunks = VECTOR_DB.search(query, k=5)
    return {"rag_context": "\n".join(chunks)}


# ---- Resource Curator ----
def resource_curator(state: MapeyState):

    queries = [
        f"Best courses for {state['topic']}",
        f"Projects for {state['topic']}",
        f"Interview prep for {state['topic']}"
    ]

    links = []
    for q in queries:
        links.append(web_search.invoke(q))

    return {"resources": "\n".join(links)}


# ---- Validator ----
def validator(state: MapeyState):

    prompt = PromptTemplate.from_template("""
You are a senior career architect and learning program designer.

Your task is to synthesize all information into a
realistic, high-impact, execution-ready career roadmap.

Inputs:

Curriculum Plan:
{curriculum}

Resume & Knowledge Context (from RAG):
{rag_context}

Learning Resources:
{resources}

Create a FINAL ROADMAP with the following structure:

1. Roadmap Overview
   - Target role readiness strategy
   - Overall timeline (weeks or months)

2. Phase-wise Plan (for each phase)
   For each phase include:
   - Objectives
   - Skills to master
   - Concepts to understand
   - Tools to practice
   - Mini-projects
   - Capstone (if applicable)

3. Weekly Study Plan (high-level)
   - What to focus on each week
   - Balance of theory vs hands-on

4. Project Portfolio Strategy
   - Projects mapped to hiring signals
   - What each project should demonstrate

5. Evaluation Metrics
   - How to test readiness
   - Benchmarks for moving to next phase

6. Interview Preparation Integration
   - When to start interview prep
   - Topics per phase

7. Adaptation Rules
   - What to do if user is ahead/behind schedule

8. Final Outcome
   - What roles user should apply for
   - What confidence level to expect

Rules:
- Be realistic and practical.
- Prioritize depth over covering too many topics.
- Optimize for hiring success, not academic completeness.
""")

    chain = prompt | llm | parser

    roadmap = chain.invoke({
        "curriculum": state["curriculum"],
        "rag_context": state.get("rag_context", "Not provided"),
        "resources": state["resources"]
    })

    return {"roadmap": roadmap}


def curriculum_planner(state: MapeyState):

    prompt = PromptTemplate.from_template("""
You are a senior learning designer and technical mentor.

Your task is to convert skill gap analysis and role analysis
into a practical, dependency-aware learning curriculum.

Inputs:

Skill Gap Report:
{skill_gaps}

Role & Industry Analysis:
{analysis}

Design a structured multi-phase curriculum with:

For EACH PHASE include:

1. Phase Name
2. Purpose (why this phase exists)
3. Prerequisites
4. Skills & Concepts to Learn
   - Ordered by dependency
5. Tools & Technologies
6. Hands-on Practice
   - Exercises
   - Mini-projects
7. Capstone or Milestone Project
8. Estimated Time (weeks)
9. Completion Criteria
   - What proves readiness to move forward

Also provide:

10. Overall Timeline Strategy
    - How phases connect
    - Where specialization begins

11. Optional Fast-Track Paths
    - What can be skipped if user is strong

Rules:
- Avoid dumping too many topics in one phase.
- Focus on skill stacking and reinforcement.
- Optimize for job-readiness, not academic coverage.
""")

    chain = prompt | llm | parser

    curriculum = chain.invoke({
        "skill_gaps": state["skill_gaps"],
        "analysis": state["analysis"]
    })

    return {"curriculum": curriculum}



# ======================================================
# LANGGRAPH
# ======================================================

graph = StateGraph(MapeyState)

graph.add_node("topic_analyzer", topic_analyzer)
graph.add_node("skill_gap_agent", skill_gap_agent)
graph.add_node("curriculum_planner", curriculum_planner)
graph.add_node("rag_retriever", rag_retriever)
graph.add_node("resource_curator", resource_curator)
graph.add_node("validator", validator)

graph.set_entry_point("topic_analyzer")

graph.add_edge("topic_analyzer", "skill_gap_agent")
graph.add_edge("skill_gap_agent", "curriculum_planner")
graph.add_edge("curriculum_planner", "rag_retriever")
graph.add_edge("rag_retriever", "resource_curator")
graph.add_edge("resource_curator", "validator")
graph.add_edge("validator", END)

Mapey_app = graph.compile()


# ======================================================
# STREAMLIT UI
# ======================================================

st.title("🧠 Mapey v3 — Agentic Career Roadmap Generator")

with st.sidebar:
    st.header("🎯 Inputs")
    role = st.text_input("Target Role", "ML Engineer")
    jd_text = st.text_area("Job Description (optional)", height=200)
    resume_file = st.file_uploader("Upload Resume (PDF/TXT)")

if resume_file:
    resume_text = read_resume_file(resume_file)

    chunks = chunk_text(resume_text)
    VECTOR_DB.add_texts(chunks)

    st.success("Resume processed and stored in Vector DB")

if st.button("🚀 Generate Roadmap"):

    if not resume_file:
        st.error("Upload resume first")
    else:
        with st.spinner("Running multi-agent system..."):

            result = Mapey_app.invoke({
                "topic": role,
                "resume": resume_text,
                "jd": jd_text
            })

        st.subheader("🎯 Final Career Roadmap")
        st.markdown(result["roadmap"])

        with st.expander("🔍 Skill Gap Analysis"):
            st.write(result["skill_gaps"])

        with st.expander("📚 Curriculum Plan"):
            st.write(result["curriculum"])

        with st.expander("🌐 Resources"):
            st.write(result["resources"])


st.caption("Mapey v3 — LangGraph • RAG • FAISS • Ollama • Streamlit")
