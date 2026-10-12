import streamlit as st
import pandas as pd
from datetime import datetime

from modules.extractor import (
    extract_text_from_pdf,
    extract_text_from_url
)

from modules.nlp_processor import (
    clean_text,
    split_sentences
)

from modules.risk_analyzer import (
    train_model,
    analyze_sentences,
    calculate_overall_risk
)


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="PrivacyGuard AI",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            135deg,
            #071a16 0%,
            #0f172a 50%,
            #111827 100%
        );
        color: #f8fafc;
    }

    [data-testid="stSidebar"] {
        background-color: #0b1220;
        border-right: 1px solid #263449;
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #f8fafc;
    }

    .subtitle {
        font-size: 16px;
        color: #a7b5c9;
    }

    .info-card {
        background: rgba(30, 41, 59, 0.85);
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #334155;
        margin-bottom: 10px;
    }

    .info-card h4 {
        color: #cbd5e1;
        margin-bottom: 8px;
    }

    .info-card h2 {
        color: #ffffff;
        margin: 0;
        font-size: 30px;
    }

    div.stButton > button {
        border-radius: 9px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "logged_in": False,
    "page": "Dashboard",
    "results": None,
    "overall_score": 0,
    "overall_level": "Low",
    "policy_text": "",
    "analysis_history": [],
    "current_analysis": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <div style="text-align:center; padding-top:55px;">
            <div style="font-size:65px;">🔐</div>
            <div class="main-title">PrivacyGuard AI</div>
            <div class="subtitle">
                Intelligent Privacy Policy Risk Analysis
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    left, middle, right = st.columns([1, 1.2, 1])

    with middle:

        with st.container(border=True):

            st.subheader("Welcome Back")
            st.caption("Login to access your privacy dashboard.")

            username = st.text_input(
                "Username",
                placeholder="Enter username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            if st.button(
                "Login",
                use_container_width=True
            ):

                if (
                    username == "admin"
                    and password == "privacy123"
                ):

                    st.session_state.logged_in = True
                    st.session_state.page = "Dashboard"

                    st.rerun()

                else:

                    st.error("Invalid username or password.")

    st.stop()


# =====================================================
# LOAD ML MODEL
# =====================================================

@st.cache_resource
def load_model():

    return train_model()


try:

    model, accuracy = load_model()

except Exception as e:

    st.error(f"Could not load ML model: {e}")
    st.stop()


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:15px 0;">
            <div style="font-size:45px;">🔐</div>
            <h2 style="color:#f8fafc;">PrivacyGuard AI</h2>
            <p style="color:#94a3b8;">
                Privacy Risk Intelligence
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("NAVIGATION")

    pages = [
        "Dashboard",
        "Analyze Policy",
        "Risk Analysis",
        "Reports"
    ]

    for page_name in pages:

        icons = {
            "Dashboard": "🏠",
            "Analyze Policy": "🔍",
            "Risk Analysis": "📊",
            "Reports": "📄"
        }

        if st.button(
            f"{icons[page_name]}  {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True
        ):

            st.session_state.page = page_name
            st.rerun()

    st.divider()

    st.caption("MODEL INFORMATION")

    st.metric(
        "ML Model Accuracy",
        f"{accuracy:.1%}"
    )

    st.caption(
        "Accuracy is measured on the project's test split."
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.page = "Dashboard"
        st.rerun()


# =====================================================
# SHARED DATA
# =====================================================

results = st.session_state.results or []

risk_counts = {
    "Low": 0,
    "Medium": 0,
    "High": 0
}

for result in results:

    risk = result.get("risk", "Medium")

    if risk in risk_counts:
        risk_counts[risk] += 1


# =====================================================
# DASHBOARD
# =====================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        '<div class="main-title">Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Monitor privacy policy analysis and risk indicators.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # Dashboard cards

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Policies Analyzed",
            len(st.session_state.analysis_history)
        )

    with col2:
        st.metric(
            "High-Risk Sentences",
            risk_counts["High"]
        )

    with col3:
        st.metric(
            "Medium-Risk Sentences",
            risk_counts["Medium"]
        )

    with col4:
        st.metric(
            "Low-Risk Sentences",
            risk_counts["Low"]
        )

    st.divider()

    left, right = st.columns([1.2, 1])

    with left:

        st.subheader("📊 Current Risk Overview")

        if results:

            st.metric(
                "Overall Risk Score",
                f'{st.session_state.overall_score}/100',
                help=(
                    "Project-defined score calculated from "
                    "the sentence risk levels."
                )
            )

            st.progress(
                min(
                    max(
                        st.session_state.overall_score / 100,
                        0.0
                    ),
                    1.0
                )
            )

            st.write(
                f"**Risk Level:** "
                f"{st.session_state.overall_level}"
            )

            st.write(
                f"**Analyzed Sentences:** {len(results)}"
            )

        else:

            st.info(
                "No analysis available yet. "
                "Open Analyze Policy to get started."
            )

    with right:

        st.subheader("📈 Risk Distribution")

        if results:

            chart_df = pd.DataFrame({
                "Risk Level": list(risk_counts.keys()),
                "Sentences": list(risk_counts.values())
            })

            st.bar_chart(
                chart_df.set_index("Risk Level")
            )

        else:

            st.info(
                "The risk chart will appear after analysis."
            )

    st.divider()

    st.subheader("🚀 Quick Actions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔍 Analyze a Policy",
            use_container_width=True
        ):

            st.session_state.page = "Analyze Policy"
            st.rerun()

    with col2:

        if st.button(
            "📄 View Reports",
            use_container_width=True
        ):

            st.session_state.page = "Reports"
            st.rerun()

    st.divider()

    st.caption(
        "PrivacyGuard AI provides preliminary, "
        "model-based privacy risk indicators. "
        "It does not certify legal compliance."
    )


# =====================================================
# ANALYZE POLICY
# =====================================================

elif st.session_state.page == "Analyze Policy":

    st.markdown(
        '<div class="main-title">Analyze Privacy Policy</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Upload a PDF, fetch a policy from a URL, '
        'or paste policy text.'
        '</div>',
        unsafe_allow_html=True
    )

    input_method = st.radio(
        "Choose input method",
        [
            "Enter Text",
            "Upload PDF",
            "Privacy Policy URL"
        ],
        horizontal=True
    )

    policy_text = ""

    # TEXT INPUT

    if input_method == "Enter Text":

        policy_text = st.text_area(
            "Privacy Policy Text",
            value=st.session_state.policy_text,
            height=250,
            placeholder=(
                "Paste the privacy policy text here..."
            )
        )

        st.session_state.policy_text = policy_text

    # PDF INPUT

    elif input_method == "Upload PDF":

        uploaded_file = st.file_uploader(
            "Upload a privacy policy PDF",
            type=["pdf"]
        )

        if uploaded_file is not None:

            try:

                policy_text = extract_text_from_pdf(
                    uploaded_file
                )

                if policy_text and policy_text.strip():

                    st.success("PDF text extracted successfully.")

                    with st.expander("Preview extracted text"):
                        st.write(policy_text[:3000])

                else:

                    st.warning(
                        "No readable text found. "
                        "The PDF may contain scanned images."
                    )

            except Exception as e:

                st.error(f"PDF extraction failed: {e}")

    # URL INPUT

    else:

        url = st.text_input(
            "Privacy Policy URL",
            placeholder="https://example.com/privacy"
        )

        if st.button(
            "🌐 Fetch Policy",
            use_container_width=True
        ):

            if not url.strip():

                st.warning("Please enter a URL.")

            elif not url.strip().lower().startswith(
                ("https://", "http://")
            ):

                st.warning(
                    "Enter a valid URL starting with "
                    "http:// or https://."
                )

            else:

                try:

                    fetched_text = extract_text_from_url(
                        url.strip()
                    )

                    if fetched_text and fetched_text.strip():

                        st.session_state.policy_text = fetched_text

                        st.success(
                            "Privacy policy fetched successfully."
                        )

                    else:

                        st.warning(
                            "No readable text was found at this URL."
                        )

                except Exception as e:

                    st.error(f"URL extraction failed: {e}")

        policy_text = st.session_state.policy_text

        if policy_text:

            with st.expander("Preview fetched text"):
                st.write(policy_text[:3000])

    st.divider()

    if st.button(
        "🚀 Analyze Privacy Policy",
        type="primary",
        use_container_width=True
    ):

        if not policy_text or not policy_text.strip():

            st.warning(
                "Please provide policy text before analysis."
            )

        else:

            with st.spinner(
                "Analyzing policy sentences..."
            ):

                try:

                    cleaned_text = clean_text(policy_text)

                    sentences = split_sentences(cleaned_text)

                    sentences = [
                        sentence.strip()
                        for sentence in sentences
                        if sentence and sentence.strip()
                    ]

                    if not sentences:

                        st.warning(
                            "No valid sentences found. "
                            "Try providing more policy text."
                        )

                    else:

                        analysis_results = analyze_sentences(
                            model,
                            sentences
                        )

                        score, level = calculate_overall_risk(
                            analysis_results
                        )

                        if not analysis_results:

                            st.warning(
                                "The model did not produce any results."
                            )

                        else:

                            st.session_state.results = analysis_results

                            st.session_state.overall_score = score

                            st.session_state.overall_level = level

                            st.session_state.current_analysis = {
                                "date": datetime.now().strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "score": score,
                                "level": level,
                                "sentences": len(analysis_results)
                            }

                            st.session_state.analysis_history.append(
                                st.session_state.current_analysis.copy()
                            )

                            st.success(
                                "Analysis completed successfully!"
                            )

                            st.session_state.page = "Risk Analysis"

                            st.rerun()

                except Exception as e:

                    st.error(
                        f"Analysis failed: {e}"
                    )


# =====================================================
# RISK ANALYSIS
# =====================================================

elif st.session_state.page == "Risk Analysis":

    st.markdown(
        '<div class="main-title">Risk Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Review the overall score, risk categories, '
        'and flagged statements.'
        '</div>',
        unsafe_allow_html=True
    )

    if not results:

        st.info(
            "No analysis results yet. "
            "Go to Analyze Policy and analyze a policy first."
        )

        if st.button("Analyze Policy"):

            st.session_state.page = "Analyze Policy"
            st.rerun()

    else:

        # OVERALL SCORE

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Overall Risk Score",
                f'{st.session_state.overall_score}/100'
            )

        with col2:

            st.metric(
                "Risk Level",
                st.session_state.overall_level
            )

        with col3:

            st.metric(
                "Sentences Analyzed",
                len(results)
            )

        st.progress(
            min(
                max(
                    st.session_state.overall_score / 100,
                    0.0
                ),
                1.0
            )
        )

        st.caption(
            "Score is a project-defined indicator, "
            "not a validated legal or security rating."
        )

        st.divider()

        # RISK DISTRIBUTION

        st.subheader("📊 Risk Distribution")

        risk_df = pd.DataFrame({
            "Risk Level": list(risk_counts.keys()),
            "Sentence Count": list(risk_counts.values())
        })

        left, right = st.columns(2)

        with left:

            st.bar_chart(
                risk_df.set_index("Risk Level")
            )

        with right:

            st.dataframe(
                risk_df,
                use_container_width=True,
                hide_index=True
            )

        st.divider()

        # CATEGORY ANALYSIS

        st.subheader("📋 Category-wise Analysis")

        category_data = {}

        for result in results:

            category = result.get(
                "category",
                "Unknown"
            )

            risk = result.get(
                "risk",
                "Medium"
            )

            if category not in category_data:

                category_data[category] = {
                    "Low": 0,
                    "Medium": 0,
                    "High": 0
                }

            if risk in category_data[category]:

                category_data[category][risk] += 1

        category_rows = []

        for category, values in category_data.items():

            total = sum(values.values())

            category_rows.append({
                "Category": category,
                "Low": values["Low"],
                "Medium": values["Medium"],
                "High": values["High"],
                "Total": total
            })

        category_df = pd.DataFrame(category_rows)

        if not category_df.empty:

            st.dataframe(
                category_df,
                use_container_width=True,
                hide_index=True
            )

            st.bar_chart(
                category_df.set_index("Category")[
                    ["Low", "Medium", "High"]
                ]
            )

        st.divider()

        # RECOMMENDATIONS

        recommendations = {

            "Personal Data Collection":
                "Collect only necessary personal information and clearly explain why it is required.",

            "Third Party Sharing":
                "Clearly disclose the third parties receiving data and the purposes of sharing.",

            "Tracking and Cookies":
                "Provide understandable cookie controls and options to reject non-essential tracking.",

            "Location Data":
                "Request location information only when necessary and provide meaningful controls.",

            "Data Retention":
                "Explain retention periods and delete information when it is no longer needed.",

            "User Rights":
                "Clearly explain how users can access, correct, or request deletion of their information.",

            "Data Security":
                "Describe appropriate safeguards for protecting personal information.",

            "Data Breach":
                "Explain incident response procedures and applicable user notification practices."
        }

        st.subheader("💡 Privacy Recommendations")

        detected_categories = sorted({
            result.get("category")
            for result in results
            if result.get("category")
        })

        for category in detected_categories:

            if category in recommendations:

                st.info(
                    f"**{category}**\n\n"
                    f"{recommendations[category]}"
                )

        st.divider()

        # HIGH-RISK SENTENCES

        st.subheader("⚠️ High-Risk Statements")

        high_risk_results = [
            result for result in results
            if result.get("risk") == "High"
        ]

        if high_risk_results:

            for index, result in enumerate(
                high_risk_results,
                start=1
            ):

                with st.expander(
                    f"High Risk Statement {index}"
                ):

                    st.write(
                        result.get("sentence", "")
                    )

                    st.caption(
                        "Predicted category: "
                        f'{result.get("category", "Unknown")}'
                    )

        else:

            st.success(
                "No statements were assigned the High risk label."
            )

        st.divider()

        # SENTENCE-WISE TABLE

        st.subheader("🔎 Sentence-wise Analysis")

        sentence_df = pd.DataFrame([
            {
                "Sentence": result.get("sentence", ""),
                "Category": result.get("category", "Unknown"),
                "Risk": result.get("risk", "Medium")
            }
            for result in results
        ])

        risk_filter = st.selectbox(
            "Filter by risk level",
            ["All", "High", "Medium", "Low"]
        )

        if risk_filter != "All":

            filtered_df = sentence_df[
                sentence_df["Risk"] == risk_filter
            ]

        else:

            filtered_df = sentence_df

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# REPORTS
# =====================================================

elif st.session_state.page == "Reports":

    st.markdown(
        '<div class="main-title">Reports</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'View analysis history and export the latest results.'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.analysis_history:

        st.subheader("📜 Session Analysis History")

        history_df = pd.DataFrame(
            st.session_state.analysis_history
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No analysis history available in this session."
        )

    st.divider()

    if results:

        st.subheader("📥 Download Latest Analysis")

        report_df = pd.DataFrame([
            {
                "Sentence": result.get("sentence", ""),
                "Category": result.get("category", "Unknown"),
                "Risk": result.get("risk", "Medium")
            }
            for result in results
        ])

        csv_data = report_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="⬇️ Download CSV Report",
            data=csv_data,
            file_name="privacyguard_analysis_report.csv",
            mime="text/csv",
            use_container_width=True
        )

        summary_df = pd.DataFrame([
            {
                "Risk Score": st.session_state.overall_score,
                "Risk Level": st.session_state.overall_level,
                "Sentences Analyzed": len(results),
                "Generated At": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }
        ])

        summary_csv = summary_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="⬇️ Download Risk Summary",
            data=summary_csv,
            file_name="privacyguard_risk_summary.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:

        st.warning(
            "Analyze a policy before downloading a report."
        )

    st.divider()

    st.caption(
        "Analysis history is currently stored for this "
        "Streamlit session only. It is not permanently saved."
    )