
import streamlit as st
import plotly.graph_objects as go

from agents.risk_agent import analyse_all_students
from agents.explanation_agent import generate_explanation
from agents.recovery_agent import calculate_projected_risk
from agents.mentor_agent import generate_mentor_note

from agents.history_agent import (
    generate_historical_report,
    generate_progress_summary
)

from utils.database import (
    create_tables,
    save_risk_record,
    save_explanation,
    save_mentor_record
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="EarlyAlert | Academic Risk System",
    page_icon="🎓",
    layout="wide"
)

create_tables()


# ==================================================
# HEADER
# ==================================================

st.title("🎓 EarlyAlert")

st.subheader(
    "AI-Powered Academic Risk Early Warning System"
)

st.write(
    "EarlyAlert identifies students who may need academic "
    "support using attendance, internal marks, and "
    "assignment performance."
)

st.info(
    "EarlyAlert is a mentor-support tool. Risk levels are "
    "early warning indicators, not permanent labels of "
    "student ability."
)

st.divider()


# ==================================================
# LOAD STUDENT DATA
# ==================================================

@st.cache_data
def load_student_data():
    return analyse_all_students()


students = load_student_data()

if not students:
    st.error("No student records found. Check your dataset.")
    st.stop()


# ==================================================
# SAVE RISK RECORDS TO DATABASE
# ==================================================

if "risk_records_saved" not in st.session_state:

    try:

        for student in students:
            save_risk_record(student)

        st.session_state["risk_records_saved"] = True

    except Exception as error:

        st.error(
            f"Database error while saving risk records: {error}"
        )


# ==================================================
# DASHBOARD METRICS
# ==================================================

total_students = len(students)

high_risk = sum(
    1 for student in students
    if student["level"] == "High"
)

medium_risk = sum(
    1 for student in students
    if student["level"] == "Medium"
)

low_risk = sum(
    1 for student in students
    if student["level"] == "Low"
)


st.header("📊 Academic Risk Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", total_students)
col2.metric("High Risk", high_risk)
col3.metric("Medium Risk", medium_risk)
col4.metric("Low Risk", low_risk)


st.divider()


# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.title("🔍 Student Filters")

departments = sorted(
    set(student["dept"] for student in students)
)

selected_department = st.sidebar.selectbox(
    "Select Department",
    ["All"] + departments
)

selected_risk = st.sidebar.selectbox(
    "Select Risk Level",
    ["All", "High", "Medium", "Low"]
)


filtered_students = students

if selected_department != "All":

    filtered_students = [
        student for student in filtered_students
        if student["dept"] == selected_department
    ]


if selected_risk != "All":

    filtered_students = [
        student for student in filtered_students
        if student["level"] == selected_risk
    ]


# ==================================================
# STUDENT RISK OVERVIEW
# ==================================================

st.header("👨‍🎓 Student Risk Overview")

if not filtered_students:

    st.warning(
        "No students found for the selected filters."
    )

else:

    for student in filtered_students:

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(4)

            col1.write(f"**{student['name']}**")

            col2.write(
                f"ID: {student['student_id']}"
            )

            col3.write(
                f"Department: {student['dept']}"
            )

            col4.write(
                f"Risk: {student['level']} "
                f"({student['score']})"
            )


st.divider()


# ==================================================
# INDIVIDUAL STUDENT SELECTION
# ==================================================

st.header("🔎 Individual Student Analysis")

student_options = {
    f"{student['student_id']} - {student['name']}": student
    for student in filtered_students
}

if not student_options:

    st.warning(
        "Select different filters to view student details."
    )

    st.stop()


selected_student_name = st.selectbox(
    "Choose a student",
    list(student_options.keys())
)

selected_student = student_options[selected_student_name]

selected_id = selected_student["student_id"]


# ==================================================
# STUDENT DETAILS
# ==================================================

st.subheader("Student Details")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Student ID",
    selected_id
)

col2.metric(
    "Department",
    selected_student["dept"]
)

col3.metric(
    "Semester",
    selected_student["semester"]
)

col4.metric(
    "Risk Score",
    selected_student["score"]
)


risk_level = selected_student["level"]

if risk_level == "High":

    st.error(f"Risk Level: {risk_level}")

elif risk_level == "Medium":

    st.warning(f"Risk Level: {risk_level}")

else:

    st.success(f"Risk Level: {risk_level}")


# ==================================================
# CONTRIBUTING FACTORS
# ==================================================

st.subheader("⚠️ Contributing Factors")

if selected_student["reasons"]:

    for reason in selected_student["reasons"]:
        st.write(f"• {reason}")

else:

    st.write("No major risk factors identified.")


# ==================================================
# SUBJECT-WISE ANALYSIS
# ==================================================

st.subheader("📚 Subject-wise Academic Analysis")

for subject in selected_student["subject_analysis"]:

    with st.expander(subject["subject"]):

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average Attendance",
            f"{subject['attendance_average']:.1f}%"
        )

        col2.metric(
            "Average Marks",
            f"{subject['marks_average']:.1f}"
        )

        col3.metric(
            "Missing Assignments",
            subject["missing_assignments"]
        )

        st.write(
            f"Attendance Trend: "
            f"{subject['attendance_trend']}"
        )

        st.write(
            f"Marks Trend: "
            f"{subject['marks_trend']}"
        )

        st.progress(
            min(
                max(int(subject["attendance_average"]), 0),
                100
            )
        )


st.divider()


# ==================================================
# HISTORICAL ACADEMIC PERFORMANCE REPORT
# ==================================================

st.header("📈 Historical Academic Performance")

st.write(
    "Track weekly attendance, internal marks, "
    "assignment completion, and estimated risk trends."
)

history = generate_historical_report(selected_id)

if history:

    summary = generate_progress_summary(history)

    # ----------------------------------------------
    # PROGRESS SUMMARY
    # ----------------------------------------------

    st.subheader("📊 Progress Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Attendance Change",
        f"{summary['attendance_change']}%",
        delta=f"{summary['attendance_change']}%"
    )

    col2.metric(
        "Marks Change",
        f"{summary['marks_change']}",
        delta=f"{summary['marks_change']}"
    )

    col3.metric(
        "Latest Weekly Risk",
        summary["latest_risk"]
    )

    st.write(summary["attendance_status"])

    st.write(summary["marks_status"])

    # ----------------------------------------------
    # ATTENDANCE AND MARKS CHART
    # ----------------------------------------------

    st.subheader(
        "Weekly Attendance and Internal Marks"
    )

    weeks = [
        f"Week {item['week']}"
        for item in history
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=weeks,
            y=[
                item["attendance"]
                for item in history
            ],
            mode="lines+markers",
            name="Attendance (%)"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=weeks,
            y=[
                item["marks"]
                for item in history
            ],
            mode="lines+markers",
            name="Internal Marks"
        )
    )

    fig.update_layout(
        xaxis_title="Academic Week",
        yaxis_title="Percentage / Marks",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ----------------------------------------------
    # ASSIGNMENT SUBMISSION CHART
    # ----------------------------------------------

    st.subheader(
        "Assignment Submission Progress"
    )

    assignment_fig = go.Figure()

    assignment_fig.add_trace(
        go.Bar(
            x=weeks,
            y=[
                item["assignments_submitted"]
                for item in history
            ],
            name="Submitted"
        )
    )

    assignment_fig.add_trace(
        go.Bar(
            x=weeks,
            y=[
                item["assignments_total"]
                - item["assignments_submitted"]
                for item in history
            ],
            name="Missing"
        )
    )

    assignment_fig.update_layout(
        barmode="stack",
        xaxis_title="Academic Week",
        yaxis_title="Number of Assignments"
    )

    st.plotly_chart(
        assignment_fig,
        use_container_width=True
    )

    # ----------------------------------------------
    # WEEKLY RISK TREND
    # ----------------------------------------------

    st.subheader(
        "Weekly Academic Risk Trend"
    )

    risk_fig = go.Figure()

    risk_fig.add_trace(
        go.Scatter(
            x=weeks,
            y=[
                item["risk_score"]
                for item in history
            ],
            mode="lines+markers",
            name="Weekly Risk Score",
            fill="tozeroy"
        )
    )

    risk_fig.update_layout(
        xaxis_title="Academic Week",
        yaxis_title="Estimated Risk Score",
        yaxis=dict(range=[0, 100])
    )

    st.plotly_chart(
        risk_fig,
        use_container_width=True
    )

else:

    st.warning(
        "No historical records found for this student."
    )


st.divider()


# ==================================================
# AI-POWERED EXPLANATION AGENT
# ==================================================

st.header("🤖 AI-Powered Academic Explanation")

st.write(
    "Generate an AI explanation of why this student "
    "may need academic support."
)

explanation_key = f"ai_explanation_{selected_id}"

if st.button(
    "✨ Generate AI Explanation",
    type="primary",
    key=f"generate_ai_{selected_id}"
):

    with st.spinner(
        "AI Agent is analysing student performance..."
    ):

        explanation = generate_explanation(
            selected_student
        )

        st.session_state[explanation_key] = explanation

        if (
            explanation
            and not explanation.startswith(
                "Unable to generate AI explanation."
            )
        ):

            try:

                save_explanation(
                    selected_id,
                    explanation
                )

            except Exception as error:

                st.warning(
                    f"Could not save explanation: {error}"
                )


saved_explanation = st.session_state.get(
    explanation_key
)

if saved_explanation:

    if saved_explanation.startswith(
        "Unable to generate AI explanation."
    ):

        st.error(saved_explanation)

    else:

        st.success(
            "AI explanation generated successfully!"
        )

        st.markdown(saved_explanation)

else:

    st.info(
        "Click the button above to generate an AI explanation."
    )


st.divider()


# ==================================================
# WHAT-IF RECOVERY SIMULATOR
# ==================================================

st.header("🔄 What-if Recovery Path Simulator")

st.write(
    "Explore how improvements in attendance, marks, "
    "and assignment completion could affect the "
    "student's estimated risk score."
)

attendance_target = st.slider(
    "Target Attendance Percentage",
    min_value=50,
    max_value=100,
    value=85,
    step=5,
    key=f"attendance_target_{selected_id}"
)

marks_improvement = st.slider(
    "Expected Marks Improvement",
    min_value=0,
    max_value=30,
    value=10,
    step=5,
    key=f"marks_improvement_{selected_id}"
)

complete_missing = st.checkbox(
    "Assume all missing assignments are completed",
    key=f"complete_missing_{selected_id}"
)


if st.button(
    "🚀 Simulate Recovery",
    key=f"simulate_{selected_id}"
):

    result = calculate_projected_risk(
        selected_student,
        attendance_target=attendance_target,
        marks_improvement=marks_improvement,
        complete_missing=complete_missing
    )

    st.session_state[
        f"recovery_result_{selected_id}"
    ] = result


recovery_result = st.session_state.get(
    f"recovery_result_{selected_id}"
)

if recovery_result:

    st.subheader("📈 Recovery Simulation Results")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Current Risk Score",
        recovery_result["original_score"]
    )

    col2.metric(
        "Projected Risk Score",
        recovery_result["projected_score"],
        delta=recovery_result["score_reduction"],
        delta_color="inverse"
    )

    col3.metric(
        "Projected Risk Level",
        recovery_result["projected_level"]
    )

    st.write(
        "### Subject-wise Projected Improvements"
    )

    for subject in recovery_result["projected_subjects"]:

        with st.expander(subject["subject"]):

            st.write(
                f"Projected Attendance: "
                f"{subject['projected_attendance']:.1f}%"
            )

            st.write(
                f"Projected Marks: "
                f"{subject['projected_marks']:.1f}"
            )

            st.write(
                f"Projected Missing Assignments: "
                f"{subject['projected_missing_assignments']}"
            )

    st.caption(
        "This is a simplified what-if estimate based on "
        "selected assumptions. It is not a guarantee "
        "of future academic outcomes."
    )


st.divider()


# ==================================================
# MENTOR COMMUNICATION CENTRE
# ==================================================

st.header("📩 Mentor Communication Centre")

st.write(
    "Prepare a personalised academic support message "
    "for the selected student."
)

explanation = st.session_state.get(
    explanation_key
)

if (
    not explanation
    or explanation.startswith(
        "Unable to generate AI explanation."
    )
):

    st.warning(
        "Please generate a successful AI explanation first."
    )

else:

    draft_key = f"mentor_draft_{selected_id}"

    message_key = f"mentor_message_{selected_id}"

    approval_key = f"mentor_approved_{selected_id}"

    approved_message_key = (
        f"approved_message_{selected_id}"
    )

    # ----------------------------------------------
    # GENERATE MENTOR DRAFT
    # ----------------------------------------------

    if st.button(
        "📝 Generate Mentor Communication Draft",
        key=f"create_draft_{selected_id}"
    ):

        draft = generate_mentor_note(
            selected_student,
            explanation
        )

        st.session_state[draft_key] = draft

        st.session_state[message_key] = (
            draft["message"]
        )

        st.session_state[approval_key] = False

        st.session_state.pop(
            approved_message_key,
            None
        )

    draft = st.session_state.get(draft_key)

    if draft:

        st.subheader("Mentor Message Draft")

        st.write(
            f"**Student ID:** {draft['student_id']}"
        )

        st.write(
            f"**Suggested Meeting:** "
            f"{draft['meeting_slot']}"
        )

        edited_message = st.text_area(
            "Review and edit the message",
            key=message_key,
            height=300
        )

        approved = st.session_state.get(
            approval_key,
            False
        )

        if (
            approved
            and edited_message != st.session_state.get(
                approved_message_key
            )
        ):

            st.session_state[approval_key] = False

            st.session_state.pop(
                approved_message_key,
                None
            )

            approved = False

        col1, col2 = st.columns(2)

        # ------------------------------------------
        # APPROVE MESSAGE
        # ------------------------------------------

        with col1:

            if st.button(
                "✅ Approve Message",
                key=f"approve_{selected_id}"
            ):

                st.session_state[approval_key] = True

                st.session_state[
                    approved_message_key
                ] = edited_message

                try:

                    save_mentor_record(
                        selected_id,
                        edited_message,
                        draft["meeting_slot"],
                        True
                    )

                    st.success(
                        "Mentor message approved and "
                        "saved to database!"
                    )

                except Exception as error:

                    st.error(
                        f"Could not save mentor approval: {error}"
                    )

                st.rerun()

        # ------------------------------------------
        # REJECT MESSAGE
        # ------------------------------------------

        with col2:

            if st.button(
                "❌ Reject Draft",
                key=f"reject_{selected_id}"
            ):

                st.session_state.pop(
                    draft_key,
                    None
                )

                st.session_state.pop(
                    message_key,
                    None
                )

                st.session_state.pop(
                    approval_key,
                    None
                )

                st.session_state.pop(
                    approved_message_key,
                    None
                )

                st.rerun()

        if st.session_state.get(
            approval_key,
            False
        ):

            st.success(
                "This mentor message has been approved."
            )

            st.info(
                "The message is saved as an approved draft. "
                "It has not been sent to the student."
            )

        else:

            st.warning(
                "This message is a draft and is waiting "
                "for mentor approval."
            )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "EarlyAlert | AI-Powered Academic Risk Early Warning System"
)

st.caption(
    "Designed to support early intervention, "
    "personalised guidance, and student academic improvement."
)
