import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import altair as alt

def render_teacher_view(state):
    """Render the teacher dashboard view with student monitoring and roadmap review."""
    st.title("Teacher Dashboard")
    
    # Teacher Profile and Overview
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://via.placeholder.com/150", width=150)
        st.write(f"**{state.teacher_data.get('name', 'Teacher')}**")
        st.write(f"Subjects: {', '.join(state.teacher_data.get('subjects', ['']))}")
    
    with col2:
        # Key metrics
        metric1, metric2, metric3 = st.columns(3)
        with metric1:
            st.metric(
                "Students", 
                state.teacher_data.get('student_count', 0),
                delta=state.teacher_data.get('student_count_change', 0)
            )
        with metric2:
            st.metric(
                "Avg. Progress", 
                f"{state.teacher_data.get('avg_progress', 0)}%",
                delta=state.teacher_data.get('avg_progress_change', 0)
            )
        with metric3:
            st.metric(
                "Roadmaps Pending Review", 
                state.teacher_data.get('pending_reviews', 0)
            )
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Student Overview", 
        "Roadmap Reviews", 
        "Performance Analytics",
        "Communication Hub"
    ])
    
    with tab1:
        render_student_overview(state)
        
    with tab2:
        render_roadmap_reviews(state)
        
    with tab3:
        render_performance_analytics(state)
        
    with tab4:
        render_communication_hub(state)

    # Notifications and Tasks Sidebar
    with st.sidebar:
        st.subheader("Tasks Due Today")
        for task in state.teacher_data.get('tasks_due', []):
            with st.container():
                st.warning(f"**{task.get('title', '')}**")
                st.write(task.get('description', ''))
                st.button("Complete", key=f"complete_{task.get('id', '')}")
        
        st.subheader("Recent Notifications")
        for notification in state.teacher_data.get('notifications', []):
            with st.container():
                st.info(f"**{notification.get('title', '')}**")
                st.write(notification.get('message', ''))
                st.caption(notification.get('time', 'Today'))

def render_student_overview(state):
    """Render student overview with filters and sorting options."""
    st.subheader("Student Overview")
    
    # Filters for student list
    col1, col2, col3 = st.columns(3)
    with col1:
        subject_filter = st.multiselect(
            "Filter by Subject",
            state.teacher_data.get('available_subjects', []),
            default=[]
        )
    with col2:
        progress_filter = st.slider(
            "Min Progress %",
            0, 100, 0
        )
    with col3:
        sort_by = st.selectbox(
            "Sort By",
            ["Name", "Progress (High to Low)", "Progress (Low to High)", "Last Active"]
        )
    
    # Get student list with filtering and sorting applied
    students = state.teacher_data.get('students', [])
    
    # Apply filters
    if subject_filter:
        students = [s for s in students if any(subj in s.get('subjects', []) for subj in subject_filter)]
    if progress_filter > 0:
        students = [s for s in students if s.get('progress', 0) >= progress_filter]
    
    # Apply sorting
    if sort_by == "Name":
        students = sorted(students, key=lambda s: s.get('name', ''))
    elif sort_by == "Progress (High to Low)":
        students = sorted(students, key=lambda s: s.get('progress', 0), reverse=True)
    elif sort_by == "Progress (Low to High)":
        students = sorted(students, key=lambda s: s.get('progress', 0))
    elif sort_by == "Last Active":
        students = sorted(students, key=lambda s: datetime.strptime(s.get('last_active', '2025-01-01'), '%Y-%m-%d'), reverse=True)
    
    # Display student list
    st.write(f"Showing {len(students)} students")
    
    for i, student in enumerate(students):
        with st.expander(f"{student.get('name', f'Student {i+1}')} - {student.get('progress', 0)}% Complete"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Target Exam:** {student.get('target_exam', '')}")
                st.write(f"**Subjects:** {', '.join(student.get('subjects', []))}")
                st.write(f"**Last Active:** {student.get('last_active', '')}")
                st.progress(student.get('progress', 0)/100)
                
                # Key metrics for this student
                metrics = student.get('metrics', {})
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.metric("Tasks Completed", metrics.get('tasks_completed', 0))
                with m_col2:
                    st.metric("Avg. Score", f"{metrics.get('avg_score', 0)}%")
                with m_col3:
                    st.metric("Study Hours", metrics.get('study_hours', 0))
            
            with col2:
                # Quick actions for this student
                st.button("View Roadmap", key=f"view_roadmap_{student.get('id', i)}")
                st.button("Message", key=f"msg_{student.get('id', i)}")
                st.button("Review Progress", key=f"review_{student.get('id', i)}")
            
            # Alerts for this student
            alerts = student.get('alerts', [])
            if alerts:
                st.write("**Alerts:**")
                for alert in alerts:
                    alert_type = alert.get('type', 'info')
                    if alert_type == 'warning':
                        st.warning(alert.get('message', ''))
                    elif alert_type == 'error':
                        st.error(alert.get('message', ''))
                    else:
                        st.info(alert.get('message', ''))
    
    # Students at risk section
    st.subheader("Students Requiring Attention")
    
    # Get at-risk students
    at_risk = [s for s in state.teacher_data.get('students', []) if s.get('at_risk', False)]
    
    if not at_risk:
        st.success("All students are on track!")
    else:
        for student in at_risk:
            with st.container():
                st.error(f"**{student.get('name', '')}** - {student.get('risk_reason', 'Requires attention')}")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(student.get('risk_details', ''))
                with col2:
                    st.button("Intervene", key=f"intervene_{student.get('id', '')}")

def render_roadmap_reviews(state):
    """Render roadmap review interface for teachers."""
    st.subheader("Roadmap Reviews")
    
    # Tabs for different review categories
    review_tab1, review_tab2, review_tab3 = st.tabs([
        "Pending Reviews", 
        "Recently Approved", 
        "Custom Adjustments"
    ])
    
    with review_tab1:
        # Pending reviews
        pending_reviews = state.teacher_data.get('pending_roadmaps', [])
        
        if not pending_reviews:
            st.info("No roadmaps pending review")
        else:
            st.write(f"{len(pending_reviews)} roadmaps pending review")
            
            for review in pending_reviews:
                with st.expander(f"Review for {review.get('student_name', '')}"):
                    st.write(f"**Generated:** {review.get('generated_date', '')}")
                    st.write(f"**Target Exam:** {review.get('target_exam', '')}")
                    
                    # Display roadmap summary
                    st.write("### Roadmap Summary")
                    for week in review.get('weeks', []):
                        st.write(f"**Week {week.get('week_num', '')}:** {week.get('focus', '')}")
                    
                    # Display AI recommendations
                    st.write("### AI Agent Recommendations")
                    for rec in review.get('recommendations', []):
                        st.info(f"**{rec.get('title', '')}:** {rec.get('details', '')}")
                    
                    # Review form
                    with st.form(f"review_form_{review.get('id', '')}"):
                        st.write("### Your Review")
                        
                        # Rate the roadmap
                        rating = st.slider(
                            "Rate this roadmap",
                            1, 5, 3,
                            key=f"rating_{review.get('id', '')}"
                        )
                        
                        # Subject-specific feedback
                        feedback_by_subject = {}
                        for subject in review.get('subjects', []):
                            st.write(f"**{subject} Plan:**")
                            subject_feedback = st.text_area(
                                f"Feedback for {subject}",
                                key=f"feedback_{review.get('id')}_{subject}"
                            )
                            feedback_by_subject[subject] = subject_feedback
                        
                        # Overall feedback
                        overall_feedback = st.text_area(
                            "Overall Feedback",
                            key=f"overall_{review.get('id', '')}"
                        )
                        
                        # Suggested changes
                        suggest_changes = st.checkbox(
                            "Suggest Changes",
                            key=f"suggest_{review.get('id', '')}"
                        )
                        
                        changes = ""
                        if suggest_changes:
                            changes = st.text_area(
                                "Describe suggested changes",
                                key=f"changes_{review.get('id', '')}"
                            )
                        
                        # Submit buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            submit = st.form_submit_button("Approve Roadmap")
                            if submit:
                                # Store the feedback in the state
                                if 'feedback_history' not in state:
                                    state.feedback_history = {}
                                
                                # Create a feedback object with all the details
                                feedback_data = {
                                    'roadmap_id': review.get('id', ''),
                                    'student_name': review.get('student_name', ''),
                                    'rating': rating,
                                    'subject_feedback': feedback_by_subject,
                                    'overall_feedback': overall_feedback,
                                    'changes_suggested': suggest_changes,
                                    'suggested_changes': changes if suggest_changes else "",
                                    'approved': True,
                                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                
                                # Store in state
                                state.feedback_history[review.get('id', '')] = feedback_data
                                
                                # Display custom success message with the actual feedback
                                st.success(f"Roadmap approved with your feedback: {overall_feedback}")
                                
                                # Display feedback summary
                                st.write("### Feedback Summary")
                                st.write(f"**Rating:** {rating}/5")
                                st.write(f"**Overall Feedback:** {overall_feedback}")
                                for subject, fb in feedback_by_subject.items():
                                    if fb:
                                        st.write(f"**{subject} Feedback:** {fb}")
                        
                        with col2:
                            reject = st.form_submit_button("Request Revision")
                            if reject:
                                # Store the rejection feedback
                                if 'feedback_history' not in state:
                                    state.feedback_history = {}
                                
                                # Create a feedback object for the rejection
                                feedback_data = {
                                    'roadmap_id': review.get('id', ''),
                                    'student_name': review.get('student_name', ''),
                                    'rating': rating,
                                    'subject_feedback': feedback_by_subject,
                                    'overall_feedback': overall_feedback,
                                    'changes_suggested': True,
                                    'suggested_changes': changes if suggest_changes else overall_feedback,
                                    'approved': False,
                                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                
                                # Store in state
                                state.feedback_history[review.get('id', '')] = feedback_data
                                
                                # Display custom info message with the actual feedback
                                st.info(f"Revision requested with feedback: {overall_feedback}")
                                
                                # Display feedback summary
                                st.write("### Revision Request Summary")
                                st.write(f"**Rating:** {rating}/5")
                                st.write(f"**Feedback:** {overall_feedback}")
                                if suggest_changes and changes:
                                    st.write(f"**Suggested Changes:** {changes}")
                                for subject, fb in feedback_by_subject.items():
                                    if fb:
                                        st.write(f"**{subject} Feedback:** {fb}")
    
    with review_tab2:
        # Recently approved roadmaps - now including actual feedback from history
        # First check if we have feedback history
        approved = []
        
        # Add feedback history to approved roadmaps if available
        if hasattr(state, 'feedback_history'):
            for feedback_id, feedback in state.feedback_history.items():
                if feedback['approved']:
                    approved.append({
                        'id': feedback_id,
                        'student_name': feedback['student_name'],
                        'approval_date': feedback['timestamp'],
                        'rating': feedback['rating'],
                        'feedback': feedback['overall_feedback'],
                        'subject_feedback': feedback['subject_feedback'],
                        'progress': 10,  # Placeholder progress
                        'target_exam': "Sample Exam"  # Placeholder
                    })
        
        # If no feedback history, use default data
        if not approved:
            approved = state.teacher_data.get('approved_roadmaps', [])
        
        if not approved:
            st.info("No recently approved roadmaps")
        else:
            for roadmap in approved:
                with st.expander(f"{roadmap.get('student_name', '')} - Approved on {roadmap.get('approval_date', '')}"):
                    st.write(f"**Target Exam:** {roadmap.get('target_exam', '')}")
                    st.write(f"**Your Rating:** {roadmap.get('rating', '')}/5")
                    
                    # Display your feedback
                    st.write("### Your Feedback")
                    st.write(roadmap.get('feedback', 'No feedback provided'))
                    
                    # Display subject-specific feedback if available
                    subject_feedback = roadmap.get('subject_feedback', {})
                    if subject_feedback:
                        st.write("### Subject-Specific Feedback")
                        for subject, feedback in subject_feedback.items():
                            if feedback:
                                st.write(f"**{subject}:** {feedback}")
                    
                    # Student progress on this roadmap
                    st.write("### Student Progress")
                    st.progress(roadmap.get('progress', 0)/100)
                    st.write(f"Progress: {roadmap.get('progress', 0)}%")
                    
                    # Quick actions
                    st.button("View Details", key=f"view_approved_{roadmap.get('id', '')}")
                    st.button("Message Student", key=f"msg_approved_{roadmap.get('id', '')}")
    
    # Custom Adjustments tab remains the same
    with review_tab3:
        # Custom roadmap adjustments
        st.write("### Create Custom Roadmap Adjustments")
        
        # Student selection
        selected_student = st.selectbox(
            "Select Student",
            [s.get('name', '') for s in state.teacher_data.get('students', [])]
        )
        
        # Adjustment type
        adjustment_type = st.radio(
            "Adjustment Type",
            ["Schedule Change", "Topic Reordering", "Resource Addition", "Custom Plan"]
        )
        
        # Adjustment details based on type
        if adjustment_type == "Schedule Change":
            st.write("### Schedule Adjustment")
            week = st.selectbox("Select Week", range(1, 13))
            day = st.selectbox("Select Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            adjustment = st.text_area("Describe the schedule change")
            
        elif adjustment_type == "Topic Reordering":
            st.write("### Topic Reordering")
            subject = st.selectbox("Select Subject", state.teacher_data.get('available_subjects', []))
            current_order = st.text_area("Current Topic Order (one per line)")
            new_order = st.text_area("New Topic Order (one per line)")
            
        elif adjustment_type == "Resource Addition":
            st.write("### Add Resources")
            subject = st.selectbox("Select Subject", state.teacher_data.get('available_subjects', []))
            topic = st.text_input("Topic")
            resource_type = st.selectbox("Resource Type", ["Video", "PDF", "Practice Questions", "Reference Material"])
            resource_link = st.text_input("Resource Link")
            resource_description = st.text_area("Resource Description")
            
        else:  # Custom Plan
            st.write("### Custom Study Plan")
            duration = st.selectbox("Duration", ["1 week", "2 weeks", "1 month"])
            focus_area = st.text_input("Focus Area")
            plan_details = st.text_area("Plan Details")
        
        # Submit adjustment
        if st.button("Submit Adjustment"):
            # Store the adjustment in the state
            if 'custom_adjustments' not in state:
                state.custom_adjustments = []
            
            adjustment_data = {
                'student': selected_student,
                'type': adjustment_type,
                'details': {},
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Add type-specific details
            if adjustment_type == "Schedule Change":
                adjustment_data['details'] = {
                    'week': week,
                    'day': day,
                    'adjustment': adjustment
                }
            elif adjustment_type == "Topic Reordering":
                adjustment_data['details'] = {
                    'subject': subject,
                    'current_order': current_order,
                    'new_order': new_order
                }
            elif adjustment_type == "Resource Addition":
                adjustment_data['details'] = {
                    'subject': subject,
                    'topic': topic,
                    'resource_type': resource_type,
                    'resource_link': resource_link,
                    'resource_description': resource_description
                }
            else:  # Custom Plan
                adjustment_data['details'] = {
                    'duration': duration,
                    'focus_area': focus_area,
                    'plan_details': plan_details
                }
            
            # Add to state
            state.custom_adjustments.append(adjustment_data)
            
            # Show custom success message with details
            st.success(f"Your {adjustment_type} adjustment for {selected_student} has been submitted. The AI will incorporate your changes.")
            
            # Display adjustment details
            st.write("### Adjustment Details")
            for key, value in adjustment_data['details'].items():
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")

def render_performance_analytics(state):
    """Render performance analytics for teacher view."""
    st.subheader("Performance Analytics")
    
    # Time period selection
    time_period = st.selectbox(
        "Time Period",
        ["Last Week", "Last Month", "Last 3 Months", "Current Semester"]
    )
    
    # Subject filter for analytics
    subject_filter = st.multiselect(
        "Filter by Subject",
        state.teacher_data.get('available_subjects', []),
        default=state.teacher_data.get('available_subjects', [])[:1],
        key="subject_filter_performance_analytics"
    )
    
    # Class performance overview
    st.write("### Class Performance Overview")
    
    # Create sample performance data
    perf_data = state.teacher_data.get('performance_data', {})
    
    if perf_data:
        # Overall performance chart
        overall_perf = perf_data.get('overall', [])
        if overall_perf:
            overall_df = pd.DataFrame(overall_perf)
            
            fig = px.line(
                overall_df, 
                x='week', 
                y='avg_score',
                title="Class Average Score by Week",
                labels={"week": "Week", "avg_score": "Average Score (%)"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Subject performance comparison
        subject_perf = perf_data.get('by_subject', {})
        if subject_perf and subject_filter:
            # Filter subjects
            filtered_subjects = {subj: data for subj, data in subject_perf.items() if subj in subject_filter}
            
            # Create dataframe for subject comparison
            subject_df_data = []
            for subject, scores in filtered_subjects.items():
                for week_data in scores:
                    subject_df_data.append({
                        'Subject': subject,
                        'Week': week_data.get('week', 0),
                        'Score': week_data.get('avg_score', 0)
                    })
            
            if subject_df_data:
                subject_df = pd.DataFrame(subject_df_data)
                
                fig = px.line(
                    subject_df,
                    x='Week',
                    y='Score',
                    color='Subject',
                    title="Performance by Subject"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Topic-wise performance analysis
    st.write("### Topic Performance Analysis")
    
    # Select subject for topic analysis
    topic_subject = st.selectbox(
        "Select Subject for Topic Analysis",
        state.teacher_data.get('available_subjects', [])
    )
    
    # Get topics for selected subject
    topics_data = state.teacher_data.get('topics_performance', {}).get(topic_subject, [])
    
    if topics_data:
        # Create dataframe for topic performance
        topic_df = pd.DataFrame(topics_data)
        
        # Bar chart for topic performance
        fig = px.bar(
            topic_df,
            x='topic',
            y='avg_score',
            title=f"Average Performance by Topic in {topic_subject}",
            color='avg_score',
            color_continuous_scale='RdYlGn',
            labels={"topic": "Topic", "avg_score": "Average Score (%)"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Topic strengths and weaknesses
        st.write("### Strengths and Weaknesses")
        
        if not topic_df.empty:
            # Sort topics by score
            strengths = topic_df.sort_values('avg_score', ascending=False).head(3)
            weaknesses = topic_df.sort_values('avg_score').head(3)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### Strongest Topics")
                for i, row in strengths.iterrows():
                    st.success(f"**{row['topic']}**: {row['avg_score']}%")
            
            with col2:
                st.write("#### Topics Needing Attention")
                for i, row in weaknesses.iterrows():
                    st.error(f"**{row['topic']}**: {row['avg_score']}%")
    
    # Student comparison analysis
    st.write("### Student Comparison")
    
    # Select specific students for comparison
    compare_students = st.multiselect(
        "Select Students to Compare",
        [s.get('name', '') for s in state.teacher_data.get('students', [])]
    )
    
    if compare_students:
        # Create sample comparison data
        students = state.teacher_data.get('students', [])
        selected_students = [s for s in students if s.get('name', '') in compare_students]
        
        if selected_students:
            # Create comparison dataframe
            comparison_data = []
            for student in selected_students:
                metrics = student.get('metrics', {})
                comparison_data.append({
                    'Student': student.get('name', ''),
                    'Progress': student.get('progress', 0),
                    'Avg. Score': metrics.get('avg_score', 0),
                    'Tasks Completed': metrics.get('tasks_completed', 0),
                    'Study Hours': metrics.get('study_hours', 0)
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            
            # Radar chart for comparison
            categories = ['Progress', 'Avg. Score', 'Tasks Completed', 'Study Hours']
            
            fig = go.Figure()
            
            for i, student in comparison_df.iterrows():
                fig.add_trace(go.Scatterpolar(
                    r=[
                        student['Progress'],
                        student['Avg. Score'],
                        student['Tasks Completed'],
                        student['Study Hours']
                    ],
                    theta=categories,
                    fill='toself',
                    name=student['Student']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                    ),
                ),
                showlegend=True,
                title="Student Performance Comparison"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Exam readiness prediction
    st.write("### Exam Readiness Prediction")
    
    # Select student for prediction
    readiness_student = st.selectbox(
        "Select Student",
        [s.get('name', '') for s in state.teacher_data.get('students', [])],
        key="readiness_student_selectbox"
    )
    
    # Get student data
    students = state.teacher_data.get('students', [])
    selected_student = next((s for s in students if s.get('name', '') == readiness_student), None)
    
    if selected_student:
        # Create readiness metrics
        readiness = selected_student.get('exam_readiness', {})
        
        if readiness:
            col1, col2 = st.columns(2)
            
            with col1:
                # Overall readiness gauge
                overall = readiness.get('overall', 0)
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=overall,
                    title={'text': "Overall Exam Readiness"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "red"},
                            {'range': [50, 75], 'color': "yellow"},
                            {'range': [75, 100], 'color': "green"}
                        ]
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Readiness by subject
                subjects = readiness.get('by_subject', {})
                
                if subjects:
                    subject_data = []
                    for subject, score in subjects.items():
                        subject_data.append({
                            'Subject': subject,
                            'Readiness': score
                        })
                    
                    subject_df = pd.DataFrame(subject_data)
                    
                    fig = px.bar(
                        subject_df,
                        x='Subject',
                        y='Readiness',
                        title="Exam Readiness by Subject",
                        color='Readiness',
                        color_continuous_scale='RdYlGn'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            # AI recommendations based on readiness
            recommendations = readiness.get('recommendations', [])
            
            if recommendations:
                st.write("### AI Recommendations for Improvement")
                for i, rec in enumerate(recommendations):
                    st.info(f"**{rec.get('title', f'Recommendation {i+1}')}**: {rec.get('details', '')}")

def render_communication_hub(state):
    """Render communication hub for teacher-student interaction."""
    st.subheader("Communication Hub")
    
    # Create tabs for different communication channels
    comm_tab1, comm_tab2, comm_tab3, comm_tab4 = st.tabs([
        "Messaging", 
        "Announcements", 
        "Feedback Requests",
        "Office Hours"
    ])
    
    with comm_tab1:
        # Direct messaging interface
        st.write("### Direct Messaging")
        
        # Student selection for messaging
        message_student = st.selectbox(
            "Select Student",
            [s.get('name', '') for s in state.teacher_data.get('students', [])],
            key="message_student_select"
        )
        
        # Get messages for selected student
        messages = state.teacher_data.get('messages', {}).get(message_student, [])
        
        # Message history container
        st.write("#### Message History")
        message_container = st.container()
        
        with message_container:
            for message in messages:
                sender = message.get('sender', '')
                content = message.get('content', '')
                timestamp = message.get('timestamp', '')
                
                if sender == "Teacher":
                    with st.container():
                        col1, col2 = st.columns([5, 1])
                        with col1:
                            st.info(content)
                        with col2:
                            st.caption(timestamp)
                else:
                    with st.container():
                        col1, col2 = st.columns([1, 5])
                        with col1:
                            st.caption(timestamp)
                        with col2:
                            st.success(content)
        
        # New message form
        with st.form("new_message_form"):
            st.write("#### New Message")
            message_text = st.text_area("Type your message here", key="new_message_text")
            
            # Upload attachments
            st.file_uploader("Attach Files", accept_multiple_files=True, key="message_attachments")
            
            # Message options
            col1, col2 = st.columns(2)
            with col1:
                priority = st.checkbox("Mark as Priority", key="message_priority")
            with col2:
                schedule = st.checkbox("Schedule Message", key="schedule_message")
            
            if schedule:
                schedule_date = st.date_input("Date", key="schedule_date")
                schedule_time = st.time_input("Time", key="schedule_time")
            
            # Submit button
            submit = st.form_submit_button("Send Message")
            if submit and message_text:
                st.success("Message sent successfully!")
    
    with comm_tab2:
        # Announcements for all students
        st.write("### Announcements")
        
        # View previous announcements
        announcements = state.teacher_data.get('announcements', [])
        
        if announcements:
            st.write("#### Previous Announcements")
            for announcement in announcements:
                with st.expander(f"{announcement.get('title', '')} - {announcement.get('date', '')}"):
                    st.write(announcement.get('content', ''))
                    st.caption(f"Sent to: {announcement.get('recipients', 'All Students')}")
                    
                    # Engagement metrics
                    metrics = announcement.get('metrics', {})
                    st.write(f"**Views:** {metrics.get('views', 0)}")
                    st.write(f"**Responses:** {metrics.get('responses', 0)}")
        
        # Create new announcement
        st.write("#### Create New Announcement")
        with st.form("new_announcement_form"):
            announcement_title = st.text_input("Announcement Title", key="announcement_title")
            announcement_content = st.text_area("Announcement Content", key="announcement_content")
            
            # Target audience selection
            audience = st.radio(
                "Send to",
                ["All Students", "Specific Classes", "Individual Students"]
            )
            
            if audience == "Specific Classes":
                classes = st.multiselect(
                    "Select Classes",
                    state.teacher_data.get('classes', [])
                )
            elif audience == "Individual Students":
                students = st.multiselect(
                    "Select Students",
                    [s.get('name', '') for s in state.teacher_data.get('students', [])]
                )
            
            # Announcement options
            pin_option = st.checkbox("Pin to Student Dashboard", key="pin_announcement")
            notify_option = st.checkbox("Send Email Notification", key="notify_announcement")
            
            # Submit button
            submit_announcement = st.form_submit_button("Post Announcement")
            if submit_announcement and announcement_title and announcement_content:
                st.success("Announcement posted successfully!")
    
    with comm_tab3:
        # Feedback requests from students
        st.write("### Feedback Requests")
        
        # Pending feedback requests
        feedback_requests = state.teacher_data.get('feedback_requests', [])
        
        if not feedback_requests:
            st.info("No pending feedback requests")
        else:
            for request in feedback_requests:
                with st.expander(f"Request from {request.get('student_name', '')} - {request.get('date', '')}"):
                    st.write(f"**Subject:** {request.get('subject', '')}")
                    st.write(f"**Topic:** {request.get('topic', '')}")
                    st.write(f"**Question:** {request.get('question', '')}")
                    
                    # View attachment if available
                    if request.get('attachment_url', ''):
                        st.write("**Attachment:**")
                        st.image(request.get('attachment_url', ''), width=300)
                    
                    # Provide feedback
                    with st.form(f"feedback_form_{request.get('id', '')}"):
                        feedback = st.text_area(
                            "Your Feedback",
                            key=f"feedback_{request.get('id', '')}"
                        )
                        
                        # Rating if applicable
                        if request.get('requires_rating', False):
                            rating = st.slider(
                                "Rating", 
                                1, 10, 5,
                                key=f"rating_{request.get('id', '')}"
                            )
                        
                        # Submit feedback
                        submit_feedback = st.form_submit_button("Send Feedback")
                        if submit_feedback and feedback:
                            st.success("Feedback submitted successfully!")
    
    with comm_tab4:
        # Office hours scheduling and management
        st.write("### Office Hours")
        
        # View current office hours
        office_hours = state.teacher_data.get('office_hours', [])
        
        if office_hours:
            st.write("#### Current Office Hours Schedule")
            
            # Create office hours table
            office_hours_data = []
            for slot in office_hours:
                office_hours_data.append({
                    'Day': slot.get('day', ''),
                    'Time': slot.get('time', ''),
                    'Location': slot.get('location', ''),
                    'Availability': slot.get('availability', 'Available')
                })
            
            office_df = pd.DataFrame(office_hours_data)
            st.dataframe(office_df)
        
        # Manage office hours
        st.write("#### Manage Office Hours")
        
        manage_tab1, manage_tab2 = st.tabs(["Schedule New Slot", "View Appointments"])
        
        with manage_tab1:
            # Schedule new office hours
            with st.form("new_office_hours"):
                col1, col2 = st.columns(2)
                
                with col1:
                    day = st.selectbox(
                        "Day",
                        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                    )
                    start_time = st.time_input("Start Time")