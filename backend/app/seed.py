import asyncio
from datetime import datetime
from typing import List, Dict

from .db import templates, projects, skills, runs

TEMPLATE_ID = "resume_template_v1"


def now_iso() -> str:
    return datetime.utcnow().isoformat()


def build_template_latex() -> str:
    # Your template (hidden text removed) + anchors added.
    # Anchors are comments only; do not affect formatting.
    return r"""\documentclass[letterpaper,11pt]{article}
% \usepackage{lmodern}
\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{xcolor}
\usepackage{fontawesome5}
\usepackage[scaled]{helvet}
\renewcommand\familydefault{\sfdefault}
\input{glyphtounicode}


\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.75in}
\addtolength{\evensidemargin}{-0.75in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-1.25in} % Default was -.5in
\addtolength{\textheight}{2in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Section formatting
\titleformat{\section}{
  \vspace{-5pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Subsection formatting
\titleformat{\subsection}{
  \vspace{-4pt}\scshape\raggedright\large
}{\hspace{-.15in}}{0em}{}[\color{black}\vspace{-8pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

% -------------------- CUSTOM COMMANDS --------------------
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\setlength{\footskip}{4.08003pt}

% -------------------- START OF DOCUMENT --------------------
\begin{document}

% -------------------- HEADING--------------------
\begin{flushright}
  \color{gray}
\end{flushright}

\vspace{-1pt}

\begin{center}
    \textbf{\Huge \scshape  Rishi Boppana} \\ \vspace{8pt}
    
    \small 
    \faIcon{github} \href{https://github.com/rishiboppana}{\underline{Rishi}} \quad
    \faIcon{linkedin} \href{https://www.linkedin.com/in/rishi-boppana/}{\underline{Rishi-Boppana}} \quad
    \faIcon{phone} \href{tel:+1 (650) 761-3864}{\underline{+1 (650) 761-3864}} \quad
    \faIcon{map-marker-alt} \underline {California}\quad
    \faIcon{envelope} \href{mailto:rishivisweswar.boppana@sjsu.edu}{\underline{rishivisweswar.boppana@sjsu.edu }} \quad
    
\end{center}


% -------------------- EDUCATION --------------------
\section{Education}

\textbf{San Jose State University, California} \hfill {\textbf{\textit{Jan 2025 – Dec 2027}}} \\
    Master's in Data Analytics, CGPA - 4.0

\textbf{Mahindra University} \hfill{\textbf{\textit{Oct 2020 – Jun 2024}}} \\
    B.Tech in Computer Science and Engineering

    \vspace{-10pt}

% -------------------- SKILLS --------------------
\section{Skills}

%==ANCHOR:SKILLS:BLOCK:START==
    \small{{
     \textbf{Programming Languages: }{R, Python, SQL, C, Java.} \\
     \textbf{Cloud Services: }{AWS S3, EC2, IAM, CloudFormation, Lambda, Lightsail, DynamoDB.}\\
     \textbf{Web Development: }{ExpressJS, FastAPI, Flask, Rest API, React, Redux, JavaScript, Kafka.}\\
     \textbf{Database \& Datamappers: }{MySQL, MongoDB, Pinecone, Redis, SQLAlchemy, Mongoose.}\\
    \textbf{Data Engineering: }{Snowflake, Airflow, dbt, Pandas.}\\
    \textbf{DevOps: }{Docker, Kubernetes, Postman, Git, CI/CD Pipelines.}\\
    \textbf{AI: }{LangChain, LangGraph, Fine-tuning, Ollama, Hugging Face.}\\
    \textbf{Soft Skills: }{Client Satisfaction, Project Coordination, Crisis Management, Multilingual Communication.}\\
    }}
%==ANCHOR:SKILLS:BLOCK:END==
\vspace{-10pt}
 
% -------------------- Experience --------------------
\section{Experience}

    {\textbf{San Jose State University }$|$\textit{{ California, USA}} $|$ \footnotesize\emph{Teaching Assistant}}\hfill{\textit{\textbf{Sep 2025 – Present} }}
    \resumeItemListStart
        \resumeItem{Prepared and evaluated \textbf{Python, Math} and \textbf{Pandas labs} for 33 graduate students, making sure code efficiency.}
        \resumeItem{Led \textbf{18 teaching sessions} to resolve doubts and enhance clarity in \textbf{SVM, LoRA, Linear Algebra} and \textbf{Statistics}.}
        \resumeItem{\textbf{Grading 14 Assignments }and\textbf{ 2 Labs} for the entire semester for all students in time and with diligance. }
    \resumeItemListEnd

    {\textbf{Innominds Ltd }$|$\textit{{ Hyderabad, India}} $|$ \footnotesize\emph{Data Science Intern }}\hfill{\textit{\textbf{Jun 2023 – Aug 2023} }}
    \resumeItemListStart
        \resumeItem{Solved inefficient \textbf{LiDAR} detection accuracy by applying a Python based \textbf{object detection pipeline}, improving range by 25\% and reducing system latency by 15\%, developed autonomous navigation reliability.}
        \resumeItem{Built 2 real time clustering modules using RANSAC and DBSCAN in Python, enabling \textbf{faster segmentation of 3D point-cloud data }and decrease computation time during object recognition.}
        \resumeItem{Optimized LiDAR perception models through signal filtering, feature extraction, and data preprocessing, boosting model stability and detection precision under varying environments by 30\%.}
    \resumeItemListEnd

%------------------------------------Projects-------------------------
\section{Project Work }

%==ANCHOR:PROJ:SLOT1:TITLE==
{\textbf{Airbnb Clone: }}\hfill \textit{\textbf{Oct 2025 – Nov 2025}}
\resumeItemListStart
%==ANCHOR:PROJ:SLOT1:B1==
\resumeItem{Created a \textbf{React.js} interface with\textbf{ Redux state management} for properties, dashboards, dynamic search with \textbf{lowering page latency from 1.8 s to 700 ms} and increase in overall responsiveness.}
%==ANCHOR:PROJ:SLOT1:B2==
\resumeItem{Architected \textbf{decoupled microservices} using Express.js, FastAPI, and Kafka, containerized with \textbf{Docker and Kubernetes}, guaranteeing scalable and \textbf{asynchronous backend communication}}
%==ANCHOR:PROJ:SLOT1:B3==
\resumeItem{Integrated an\textbf{ AI-driven} itinerary service using \textbf{LangChain, Ollama, and Tavily}, and validated performance with \textbf{JMeter }(200 req/s, 5 K concurrent users).}
\resumeItemListEnd
\vspace{2.5pt}

%==ANCHOR:PROJ:SLOT2:TITLE==
{\textbf{Context-Based Chat Platform:}  }\hfill \textit{\textbf{Aug 2025 – Sep 2025}}
\resumeItemListStart
%==ANCHOR:PROJ:SLOT2:B1==
\resumeItem{An intuitive React.js chat interface supporting \textbf{real-time updates} and smooth context-based message rendering.}
%==ANCHOR:PROJ:SLOT2:B2==
\resumeItem{Deployed communications through\textbf{ Kafka backend} and \textbf{Redis caching}, facilitating sub-100 ms message processing to ensure seamless message delivery and \textbf{maintain session context}.}
%==ANCHOR:PROJ:SLOT2:B3==
\resumeItem{Set up \textbf{microservices on AWS EC2} leveraging \textbf{autoscaling and load balancing}, attaining 99.9\% availability and decreasing server load by \textbf{40\% during peak traffic periods}.}
\resumeItemListEnd

%==ANCHOR:PROJ:SLOT3:TITLE==
{\textbf{Asteroid Analytics – Near-Earth Object Prediction System: }}\hfill \textit{\textbf{Mar 2025 – Jun 2025}}
\resumeItemListStart
%==ANCHOR:PROJ:SLOT3:B1==
\resumeItem{Streamlined a \textbf{real-time asteroid monitoring pipeline} using Python and \textbf{Airflow}, storing 730 days of data in \textbf{Snowflake for continuous analysis}.}
%==ANCHOR:PROJ:SLOT3:B2==
\resumeItem{Executed \textbf{dbt tests} and data validations, preserving 100\% pipeline reliability and clean analytics along with dbt ELT models using 4 \textbf{custom macros} to \textbf{automate forecasting} of future asteroid trajectories.}
%==ANCHOR:PROJ:SLOT3:B3==
\resumeItem{Designed an interactive \textbf{Tableau dashboard} of 6 visualizations showing asteroid size, speed, and proximity trends for planetary risk insights.}
\resumeItemListEnd
\vspace{2.5pt}

%================ Certifications =================
\section{Certifications}
\begin{itemize}
    \item \underline{\textbf{\href{https://www.credly.com/badges/1cab8b73-13b9-493e-833c-e5d3d1d61e9b/public_url}{AWS Certified Cloud Practitioner}}} --- Amazon Web Services.  \hfill{\textit{\textbf{Jul 2025} }}
    \item \underline{\textbf{\href{https://coursera.org/share/aa12e3dcf187571e346e089305b1ddcc}{Supervised Machine Learning: Regression and Classification}}} --- Coursera.\hfill{\textit{\textbf{Jul 2022} }}
\end{itemize}

\end{document}
"""


def normalize_skill(s: str) -> str:
    return s.strip()


def build_skills_seed() -> List[Dict]:
    # Merged from both resumes (deduped). Status verified by default.
    skill_list = [
        # Programming
        "Python", "SQL", "R", "Java", "C", "JavaScript",
        # Cloud / AWS
        "AWS", "S3", "EC2", "IAM", "CloudFormation", "Lambda", "Lightsail", "DynamoDB",
        # Web/backend
        "FastAPI", "Flask", "ExpressJS", "REST API", "React", "Redux", "Kafka",
        # Databases / stores
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "Snowflake", "Redshift", "Pinecone",
        "SQLAlchemy", "Mongoose",
        # Data Engineering
        "Airflow", "dbt", "Pandas", "ETL", "ELT", "Data Warehousing", "Feature Engineering",
        # DevOps/MLOps
        "Docker", "Kubernetes", "Git", "CI/CD", "Postman", "MLflow", "Model Monitoring", "A/B Testing",
        # ML/AI
        "SVM", "Ridge Regression", "K-Means", "Random Forest", "Gradient Boosting", "DBSCAN", "RANSAC",
        "Object Detection", "LoRA", "Fine-tuning", "Hugging Face", "LangChain", "LangGraph", "RAG", "GEval", "MCP", "Ollama",
        "Wav2Lip", "SadTalker", "Snowpark ML", "Time-Series Regression",
        # Visualization
        "Tableau", "Power BI", "Streamlit", "Plotly", "Matplotlib", "Seaborn", "JMeter",
        # Soft skills (optional)
        "Client Satisfaction", "Project Coordination", "Crisis Management", "Multilingual Communication",
    ]

    docs = []
    for name in sorted(set(normalize_skill(x) for x in skill_list)):
        docs.append({
            "name": name,
            "synonyms": [],
            "status": "verified",
            "created_at": now_iso(),
        })
    return docs


def build_projects_seed() -> List[Dict]:
    # All unique projects from BOTH resumes
    return [
        {
            "_id": "proj_airbnb_clone",
            "key": "AIRBNB",
            "title": "Airbnb Clone",
            "date_range": "Oct 2025 – Nov 2025",
            "domain_tags": ["distributed-systems", "fullstack", "microservices"],
            "skills": ["React", "Redux", "ExpressJS", "FastAPI", "Kafka", "Docker", "Kubernetes", "LangChain", "Ollama", "Tavily", "JMeter"],
            "bullets": [
                {"id": "b1", "text": r"Created a \textbf{React.js} interface with\textbf{ Redux state management} for properties, dashboards, dynamic search with \textbf{lowering page latency from 1.8 s to 700 ms} and increase in overall responsiveness.", "verified": True, "metrics": ["1.8s→700ms"], "version": 1},
                {"id": "b2", "text": r"Architected \textbf{decoupled microservices} using Express.js, FastAPI, and Kafka, containerized with \textbf{Docker and Kubernetes}, guaranteeing scalable and \textbf{asynchronous backend communication}", "verified": True, "metrics": [], "version": 1},
                {"id": "b3", "text": r"Integrated an\textbf{ AI-driven} itinerary service using \textbf{LangChain, Ollama, and Tavily}, and validated performance with \textbf{JMeter }(200 req/s, 5 K concurrent users).", "verified": True, "metrics": ["200 req/s", "5K concurrent"], "version": 1},
            ],
            "created_at": now_iso(),
            "updated_at": now_iso(),
        },
        {
            "_id": "proj_context_chat_platform",
            "key": "CHAT",
            "title": "Context-Based Chat Platform",
            "date_range": "Aug 2025 – Sep 2025",
            "domain_tags": ["distributed-systems", "real-time", "messaging"],
            "skills": ["React", "Kafka", "Redis", "AWS", "EC2", "Autoscaling", "Load Balancing"],
            "bullets": [
                {"id": "b1", "text": r"An intuitive React.js chat interface supporting \textbf{real-time updates} and smooth context-based message rendering.", "verified": True, "metrics": [], "version": 1},
                {"id": "b2", "text": r"Deployed communications through\textbf{ Kafka backend} and \textbf{Redis caching}, facilitating sub-100 ms message processing to ensure seamless message delivery and \textbf{maintain session context}.", "verified": True, "metrics": ["<100ms"], "version": 1},
                {"id": "b3", "text": r"Set up \textbf{microservices on AWS EC2} leveraging \textbf{autoscaling and load balancing}, attaining 99.9\% availability and decreasing server load by \textbf{40\% during peak traffic periods}.", "verified": True, "metrics": ["99.9%", "40%"], "version": 1},
            ],
            "created_at": now_iso(),
            "updated_at": now_iso(),
        },
        {
            "_id": "proj_asteroid_analytics",
            "key": "ASTEROID",
            "title": "Asteroid Analytics – Near-Earth Object Prediction System",
            "date_range": "Mar 2025 – Jun 2025",
            "domain_tags": ["data-engineering", "analytics", "forecasting"],
            "skills": ["Python", "Airflow", "Snowflake", "dbt", "Tableau", "Snowpark ML", "Feature Engineering", "Time-Series Regression", "ETL", "ELT"],
            "bullets": [
                {"id": "b1", "text": r"Streamlined a \textbf{real-time asteroid monitoring pipeline} using Python and \textbf{Airflow}, storing 730 days of data in \textbf{Snowflake for continuous analysis}.", "verified": True, "metrics": ["730 days"], "version": 1},
                {"id": "b2", "text": r"Executed \textbf{dbt tests} and data validations, preserving 100\% pipeline reliability and clean analytics along with dbt ELT models using 4 \textbf{custom macros} to \textbf{automate forecasting} of future asteroid trajectories.", "verified": True, "metrics": ["100%"], "version": 1},
                {"id": "b3", "text": r"Designed an interactive \textbf{Tableau dashboard} of 6 visualizations showing asteroid size, speed, and proximity trends for planetary risk insights.", "verified": True, "metrics": ["6 visualizations"], "version": 1},
                # Additional bullet variants from the second resume (kept as extra versions)
                {"id": "b4", "text": r"Developed 12+ \textbf{dbt ELT} models with \textbf{tests} and \textbf{macros} to generate clean, ML-ready features (velocity, diameter, miss-distance).", "verified": True, "metrics": ["12+"], "version": 2},
                {"id": "b5", "text": r"Implemented asteroid-approach \textbf{forecasting in Snowflake} using \textbf{Snowpark ML} with \textbf{feature engineering} and \textbf{time-series regression}, reducing prediction error by 22\% for near-Earth approach distance.", "verified": True, "metrics": ["22%"], "version": 2},
            ],
            "created_at": now_iso(),
            "updated_at": now_iso(),
        },
        {
            "_id": "proj_food_scarcity",
            "key": "FOOD",
            "title": "Food Scarcity Prediction",
            "date_range": "Sept 2025 – Nov 2025",
            "domain_tags": ["machine-learning", "public-health", "analytics"],
            "skills": ["Python", "SVM", "Ridge Regression", "K-Means", "Feature Engineering", "Model Evaluation"],
            "bullets": [
                {"id": "b1", "text": r"Analyzed USDA Food Access Atlas county-level dataset (~3,100 counties) to study limited access to healthy food.", "verified": True, "metrics": ["~3,100"], "version": 1},
                {"id": "b2", "text": r"Used \textbf{SVM} to classify counties with low vs normal food access (based on income \& distance to grocery stores), \textbf{Ridge Regression} to predict food scarcity severity scores, and \textbf{K-Means} to cluster similar high-risk county groups.", "verified": True, "metrics": [], "version": 1},
                {"id": "b3", "text": r"Models achieved 84\% SVM accuracy, R² of 0.814 for Ridge Regression, and 3 meaningful clusters showing areas impacted by low income and long travel distance to supermarkets.", "verified": True, "metrics": ["84%", "0.814", "3"], "version": 1},
            ],
            "created_at": now_iso(),
            "updated_at": now_iso(),
        },
        {
            "_id": "proj_aac_concrete",
            "key": "AAC",
            "title": "Predicting Hardened Properties and Carbon Footprint of Alkali-Activated Concrete",
            "date_range": "Jan 2024 – Mar 2024",
            "domain_tags": ["machine-learning", "regression", "sustainability"],
            "skills": ["Random Forest", "Gradient Boosting", "Feature Engineering", "Model Evaluation"],
            "bullets": [
                {"id": "b1", "text": r"Applied \textbf{Random Forest} and \textbf{Gradient Boosting} on a 1,630-sample dataset (17 features) to predict compressive strength and carbon footprint of AAC, achieving RMSE of 2.1 MPa for strength prediction and MAE of 3.4 kg CO₂/m³ for carbon footprint.", "verified": True, "metrics": ["1,630", "17", "2.1", "3.4"], "version": 1},
                {"id": "b2", "text": r"Increased predictive accuracy by 19\% by feature engineering (correlation filtering, log-scaling,interaction terms)", "verified": True, "metrics": ["19%"], "version": 1},
                {"id": "b3", "text": r"Reduced carbon-footprint prediction error by 30\% (MAPE drop), enabling more sustainable AAC material design.", "verified": True, "metrics": ["30%"], "version": 1},
            ],
            "created_at": now_iso(),
            "updated_at": now_iso(),
        },
    ]


def build_experience_seed() -> List[Dict]:
    # Optional collection if you add it later; not used by current retrieval.
    return [
        {
            "_id": "exp_sjsu_ta",
            "company": "San Jose State University",
            "location": "California, USA",
            "role": "Teaching Assistant",
            "date_range": "Sep 2025 – Present",
            "bullets": [
                r"Prepared and evaluated \textbf{Python, Math} and \textbf{Pandas labs} for 33 graduate students, making sure code efficiency.",
                r"Led \textbf{18 teaching sessions} to resolve doubts and enhance clarity in \textbf{SVM, LoRA, Linear Algebra} and \textbf{Statistics}.",
                r"\textbf{Grading 14 Assignments }and\textbf{ 2 Labs} for the entire semester for all students in time and with diligance.",
            ],
            "created_at": now_iso(),
            "updated_at": now_iso(),
        },
        {
            "_id": "exp_innominds_intern",
            "company": "Innominds Ltd",
            "location": "Hyderabad, India",
            "role": "Data Science Intern",
            "date_range": "Jun 2023 – Aug 2023",
            "bullets": [
                r"Solved inefficient \textbf{LiDAR} detection accuracy by applying a Python based \textbf{object detection pipeline}, improving range by 25\% and reducing system latency by 15\%, developed autonomous navigation reliability.",
                r"Built 2 real time clustering modules using RANSAC and DBSCAN in Python, enabling \textbf{faster segmentation of 3D point-cloud data }and decrease computation time during object recognition.",
                r"Optimized LiDAR perception models through signal filtering, feature extraction, and data preprocessing, boosting model stability and detection precision under varying environments by 30\%.",
            ],
            "created_at": now_iso(),
            "updated_at": now_iso(),
        },
        {
            "_id": "exp_nexed_mle",
            "company": "Nexed",
            "location": "California, USA",
            "role": "Machine Learning Engineer",
            "date_range": "Jun 2025 – Present",
            "bullets": [
                r"Built a prompt enhancement model for story-based video generation by \textbf{fine tuning} LLMs using \textbf{LoRA}, reducing model training time by 18\%.",
                r"Performed lipsync for 50+ generated clips using Wav2Lip and SadTalker improving \textbf{audio-speech alignment}.",
                r"Integrated \textbf{LangGraph} into the pipeline to evaluate and refine story outputs, reducing manual content review effort by ~35\%.",
                r"Worked on an end-to-end AI video generation pipeline including \textbf{story generation, lip-sync, and model evaluation} for the startup.",
            ],
            "created_at": now_iso(),
            "updated_at": now_iso(),
        },
    ]


async def upsert_many_unique(coll, docs: List[Dict], unique_field: str = "name"):
    for d in docs:
        await coll.update_one({unique_field: d[unique_field]}, {"$setOnInsert": d}, upsert=True)


async def seed_all():
    # Optional: clear previous runs but keep collections (comment out if you want)
    # await runs.delete_many({})

    # 1) Seed template
    latex = build_template_latex()
    await templates.update_one(
        {"_id": TEMPLATE_ID},
        {"$set": {
            "_id": TEMPLATE_ID,
            "name": "default_template_with_anchors",
            "latex": latex,
            "updated_at": now_iso(),
            "created_at": now_iso(),
        }},
        upsert=True
    )

    # 2) Seed skills
    skill_docs = build_skills_seed()
    await upsert_many_unique(skills, skill_docs, unique_field="name")

    # 3) Seed projects
    proj_docs = build_projects_seed()
    for p in proj_docs:
        await projects.update_one({"_id": p["_id"]}, {"$set": p}, upsert=True)

    # 4) (Optional) Seed experience into a separate collection if you add it later
    # If you want it now, create the collection in db.py: experiences = db["experiences"]
    # from .db import experiences
    # exp_docs = build_experience_seed()
    # for e in exp_docs:
    #     await experiences.update_one({"_id": e["_id"]}, {"$set": e}, upsert=True)

    print("✅ Seed complete:")
    print(f" - Template: {TEMPLATE_ID}")
    print(f" - Skills upserted: {len(skill_docs)}")
    print(f" - Projects upserted: {len(proj_docs)}")


if __name__ == "__main__":
    asyncio.run(seed_all())
