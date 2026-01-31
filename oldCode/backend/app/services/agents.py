"""
LangGraph agents for roadmap generation.
Refactored from the original Streamlit implementation.
"""
from typing import TypedDict, List
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from tavily import TavilyClient
from app.core.config import settings
from app.core.logging import get_logger
from app.services.vector_store import get_vector_store

logger = get_logger(__name__)

# Initialize LLM
llm = OllamaLLM(
    model=settings.OLLAMA_MODEL,
    temperature=settings.OLLAMA_TEMPERATURE,
    num_ctx=settings.OLLAMA_NUM_CTX,
    base_url=settings.OLLAMA_BASE_URL
)
parser = StrOutputParser()

# Initialize Tavily client
tavily_client = None
if settings.TAVILY_API_KEY:
    tavily_client = TavilyClient(api_key='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')
else:
    logger.warning("TAVILY_API_KEY not set, web search functionality will be disabled")


class MapeyState(TypedDict):
    """State schema for the LangGraph workflow."""
    topic: str
    resume: str
    jd: str
    analysis: str
    skill_gaps: str
    curriculum: str
    rag_context: str
    resources: str
    roadmap: str


@tool
def web_search(query: str) -> str:
    """Search the web for learning resources."""
    if not tavily_client:
        logger.warning("Tavily client not available, returning empty search results")
        return "Web search unavailable: API key not configured"
    
    try:
        res = tavily_client.search(query=query, max_results=5)
        urls = "\n".join(r["url"] for r in res.get("results", []))
        logger.info(f"Web search completed for query: {query[:50]}...")
        return urls
    except Exception as e:
        logger.error(f"Error in web search: {str(e)}", exc_info=True)
        return f"Error searching web: {str(e)}"


def topic_analyzer(state: MapeyState) -> dict:
    """Analyze the target role and provide expert insights."""
    logger.info(f"Running topic analyzer for: {state['topic']}")
    
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

    try:
        chain = prompt | llm | parser
        result = chain.invoke({"topic": state["topic"]})
        logger.info("Topic analyzer completed successfully")
        return {"analysis": result}
    except Exception as e:
        logger.error(f"Error in topic analyzer: {str(e)}", exc_info=True)
        return {"analysis": f"Error analyzing topic: {str(e)}"}


def skill_gap_agent(state: MapeyState) -> dict:
    """Perform skill gap analysis between resume and job requirements."""
    logger.info("Running skill gap agent")
    
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

    try:
        chain = prompt | llm | parser
        result = chain.invoke({
            "topic": state["topic"],
            "resume": state["resume"],
            "jd": state.get("jd", "Not provided")
        })
        logger.info("Skill gap agent completed successfully")
        return {"skill_gaps": result}
    except Exception as e:
        logger.error(f"Error in skill gap agent: {str(e)}", exc_info=True)
        return {"skill_gaps": f"Error performing skill gap analysis: {str(e)}"}


def rag_retriever(state: MapeyState) -> dict:
    """Retrieve relevant context from vector store."""
    logger.info("Running RAG retriever")
    
    try:
        vector_store = get_vector_store()
        query = f"Learning resources for {state['topic']} skills"
        chunks = vector_store.search(query, k=5)
        context = "\n".join(chunks) if chunks else "No relevant context found in knowledge base."
        logger.info(f"RAG retriever found {len(chunks)} relevant chunks")
        return {"rag_context": context}
    except Exception as e:
        logger.error(f"Error in RAG retriever: {str(e)}", exc_info=True)
        return {"rag_context": "Error retrieving context from knowledge base."}


def resource_curator(state: MapeyState) -> dict:
    """Curate web resources for learning."""
    logger.info("Running resource curator")
    
    queries = [
        f"Best courses for {state['topic']}",
        f"Projects for {state['topic']}",
        f"Interview prep for {state['topic']}"
    ]

    links = []
    for q in queries:
        try:
            result = web_search.invoke(q)
            links.append(result)
        except Exception as e:
            logger.warning(f"Error searching for '{q}': {str(e)}")
            links.append(f"Error searching: {str(e)}")

    resources = "\n".join(links)
    logger.info("Resource curator completed")
    return {"resources": resources}


def curriculum_planner(state: MapeyState) -> dict:
    """Create a structured learning curriculum."""
    logger.info("Running curriculum planner")
    
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

    try:
        chain = prompt | llm | parser
        result = chain.invoke({
            "skill_gaps": state["skill_gaps"],
            "analysis": state["analysis"]
        })
        logger.info("Curriculum planner completed successfully")
        return {"curriculum": result}
    except Exception as e:
        logger.error(f"Error in curriculum planner: {str(e)}", exc_info=True)
        return {"curriculum": f"Error creating curriculum: {str(e)}"}


def validator(state: MapeyState) -> dict:
    """Validate and synthesize final roadmap."""
    logger.info("Running validator to generate final roadmap")
    
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

    try:
        chain = prompt | llm | parser
        roadmap = chain.invoke({
            "curriculum": state["curriculum"],
            "rag_context": state.get("rag_context", "Not provided"),
            "resources": state["resources"]
        })
        logger.info("Validator completed successfully, roadmap generated")
        return {"roadmap": roadmap}
    except Exception as e:
        logger.error(f"Error in validator: {str(e)}", exc_info=True)
        return {"roadmap": f"Error generating roadmap: {str(e)}"}


def create_roadmap_graph() -> StateGraph:
    """Create and configure the LangGraph workflow."""
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
    
    return graph.compile()


# Create the compiled graph
roadmap_graph = create_roadmap_graph()
