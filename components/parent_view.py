import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import altair as alt

def render_parent_view(state):
    """Render the parent dashboard view with insights and feedback options."""
    st.title("Parent Dashboard")
    
    # Parent and Student Overview
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://via.placeholder.com/150", width=150)
        st.write(f"**{state.parent_data.get('name', 'Parent')}**")
    
    with col2:
        # Display student selection if multiple children
        children = state.parent_data.get('children', [])
        if len(children) > 1:
            selected_child = st.selectbox(
                "Select Child",
                [child.get('name', f'Child {i+1}') for i, child in enumerate(children)]
            )
            # Get the selected child's data
            child_data = next((child for child in children if child.get('name') == selected_child), children[0])
        else:
            child_data = children[0] if children else {}
        
        st.subheader(f"{child_data.get('name', 'Student')}")
        st.write(f"Target Exam: {child_data.get('target_exam', '')}")
        st.write(f"Grade/Class: {child_data.get('grade', '')}")
        
        # Display progress metrics
        progress = child_data.get('progress', 0)
        st.progress(progress/100)
        st.write(f"**Overall Progress: {progress}%**")
    
    # Main Dashboard Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Progress Overview", 
        "Weekly Insights", 
        "Provide Feedback", 
        "Communication"
    ])
    
    with tab1:
        render_progress_overview(state, child_data)
        
    with tab2:
        render_weekly_insights(state, child_data)
        
    with tab3:
        render_feedback_form(state, child_data)
        
    with tab4:
        render_communication_hub(state, child_data)
    
    # Notifications and Upcoming Events
    with st.sidebar:
        st.subheader("Important Notifications")
        for notification in state.parent_data.get('notifications', []):
            with st.container():
                if notification.get('priority', 'normal') == 'high':
                    st.error(notification.get('message', ''))
                else:
                    st.info(notification.get('message', ''))
                st.caption(notification.get('time', 'Today'))
        
        st.subheader("Upcoming Events")
        for event in state.parent_data.get('upcoming_events', []):
            with st.container():
                st.warning(f"**{event.get('title', '')}**")
                st.write(f"Date: {event.get('date', '')}")
                st.write(event.get('description', ''))

def render_progress_overview(state, child_data):
    """Render the progress overview section for parents."""
    st.subheader("Progress Overview")
    
    # Overall progress metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Study Plan Adherence", 
            f"{child_data.get('plan_adherence', 0)}%",
            delta=child_data.get('plan_adherence_change', 0)
        )
    
    with col2:
        st.metric(
            "Average Score", 
            f"{child_data.get('avg_score', 0)}%",
            delta=child_data.get('avg_score_change', 0)
        )
    
    with col3:
        st.metric(
            "Weekly Study Hours", 
            child_data.get('weekly_hours', 0),
            delta=child_data.get('weekly_hours_change', 0)
        )
    
    # Subject performance overview
    st.write("### Subject Performance")
    subjects = child_data.get('subjects', [])
    
    if subjects:
        # Create dataframe for subject performance
        subject_df = pd.DataFrame({
            'Subject': [subject.get('name', '') for subject in subjects],
            'Score': [subject.get('score', 0) for subject in subjects],
            'Progress': [subject.get('progress', 0) for subject in subjects]
        })
        
        # Create bar chart
        chart = alt.Chart(subject_df).mark_bar().encode(
            x=alt.X('Subject', sort=None),
            y='Score',
            color=alt.Color('Subject', legend=None)
        ).properties(
            title='Subject Performance'
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        # Show detailed subject progress
        for subject in subjects:
            with st.expander(f"{subject.get('name', '')} - {subject.get('score', 0)}%"):
                st.write(f"**Progress:** {subject.get('progress', 0)}%")
                st.progress(subject.get('progress', 0)/100)
                
                # Topics in this subject
                topics = subject.get('topics', [])
                if topics:
                    st.write("**Topics:**")
                    for topic in topics:
                        st.write(f"- {topic.get('name', '')}: {topic.get('mastery', 'In Progress')}")
                
                # Teacher comments
                comments = subject.get('teacher_comments', [])
                if comments:
                    st.write("**Teacher Comments:**")
                    for comment in comments:
                        st.info(f"{comment.get('date', '')}: {comment.get('content', '')}")
    
    # Recent assessments
    st.write("### Recent Assessments")
    assessments = child_data.get('recent_assessments', [])
    
    if not assessments:
        st.info("No recent assessments available")
    else:
        for assessment in assessments:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{assessment.get('title', '')}**")
                st.write(f"Date: {assessment.get('date', '')}")
                st.write(f"Subject: {assessment.get('subject', '')}")
            
            with col2:
                st.metric(
                    "Score", 
                    f"{assessment.get('score', 0)}%",
                    delta=assessment.get('score_change', 0) if 'score_change' in assessment else None
                )
            
            # Show details in expander
            with st.expander("See Details"):
                st.write(f"**Topics Covered:**")
                for topic in assessment.get('topics', []):
                    st.write(f"- {topic}")
                
                st.write("**Strengths:**")
                for strength in assessment.get('strengths', []):
                    st.write(f"- {strength}")
                
                st.write("**Areas for Improvement:**")
                for area in assessment.get('areas_for_improvement', []):
                    st.write(f"- {area}")
    
    # Roadmap completion
    st.write("### Study Roadmap Progress")
    roadmap = child_data.get('roadmap', {})
    
    # Show roadmap phases
    phases = roadmap.get('phases', [])
    if phases:
        # Create a timeline view
        for i, phase in enumerate(phases):
            phase_complete = phase.get('completion', 0) == 100
            phase_color = "green" if phase_complete else "blue"
            
            # Display phase as a timeline item
            col1, col2, col3 = st.columns([1, 10, 2])
            with col1:
                st.markdown(f"<div style='background-color:{phase_color};width:20px;height:20px;border-radius:50%;'></div>", unsafe_allow_html=True)
            with col2:
                st.write(f"**Phase {i+1}: {phase.get('name', '')}**")
                st.progress(phase.get('completion', 0)/100)
            with col3:
                st.write(f"{phase.get('completion', 0)}%")
            
            # Display details if expanding
            with st.expander("View Details"):
                st.write(f"**Focus Areas:** {', '.join(phase.get('focus_areas', []))}")
                st.write(f"**Duration:** {phase.get('duration', '')}")
                
                # Key milestones
                milestones = phase.get('milestones', [])
                if milestones:
                    st.write("**Key Milestones:**")
                    for milestone in milestones:
                        completed = milestone.get('completed', False)
                        icon = "✅" if completed else "⏳"
                        st.write(f"{icon} {milestone.get('description', '')}")

def render_weekly_insights(state, child_data):
    """Render weekly insights for parents to track their child's progress."""
    st.subheader("Weekly Insights")
    
    # Week selection
    weeks = [f"Week {i}" for i in range(1, child_data.get('current_week', 1) + 1)]
    selected_week = st.selectbox("Select Week", weeks, index=len(weeks)-1)
    
    # Get weekly data
    week_index = int(selected_week.split()[1]) - 1
    weekly_data = child_data.get('weekly_data', [])
    
    if week_index < len(weekly_data):
        week_data = weekly_data[week_index]
        
        # Weekly summary
        st.write("### Weekly Summary")
        st.write(week_data.get('summary', 'No summary available for this week.'))
        
        # Key metrics for the week
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Study Hours", 
                week_data.get('study_hours', 0),
                delta=week_data.get('study_hours_change', 0)
            )
        
        with col2:
            st.metric(
                "Tasks Completed", 
                f"{week_data.get('tasks_completed', 0)}/{week_data.get('total_tasks', 0)}",
                delta=week_data.get('tasks_completed_change', 0)
            )
        
        with col3:
            st.metric(
                "Average Score", 
                f"{week_data.get('avg_score', 0)}%",
                delta=week_data.get('avg_score_change', 0)
            )
        
        # Subject time distribution
        st.write("### Time Allocation by Subject")
        subject_hours = week_data.get('subject_hours', {})
        
        if subject_hours:
            # Create a pie chart of time distribution
            subject_df = pd.DataFrame({
                'Subject': list(subject_hours.keys()),
                'Hours': list(subject_hours.values())
            })
            
            fig = px.pie(
                subject_df, 
                values='Hours', 
                names='Subject',
                title='Study Time Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Weekly highlights
        st.write("### Weekly Highlights")
        highlights = week_data.get('highlights', [])
        
        if not highlights:
            st.info("No highlights available for this week")
        else:
            for highlight in highlights:
                st.write(f"- **{highlight.get('subject', '')}**: {highlight.get('description', '')}")
        
        # Areas needing attention
        st.write("### Areas Needing Attention")
        attention_areas = week_data.get('attention_areas', [])
        
        if not attention_areas:
            st.success("No areas requiring special attention this week")
        else:
            for area in attention_areas:
                st.error(f"**{area.get('subject', '')}**: {area.get('description', '')}")
                
                # Show recommendations if available
                recommendations = area.get('recommendations', [])
                if recommendations:
                    st.write("**Recommendations:**")
                    for rec in recommendations:
                        st.info(f"- {rec}")
        
        # Weekly schedule adherence
        st.write("### Schedule Adherence")
        schedule_data = week_data.get('schedule_adherence', {})
        
        # Create schedule adherence visualization
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        adherence_data = []
        
        for day in days:
            adherence_data.append({
                'Day': day,
                'Adherence': schedule_data.get(day, 0)
            })
        
        adherence_df = pd.DataFrame(adherence_data)
        
        # Create bar chart for schedule adherence
        chart = alt.Chart(adherence_df).mark_bar().encode(
            x=alt.X('Day', sort=None),
            y='Adherence',
            color=alt.condition(
                alt.datum.Adherence < 70,
                alt.value('red'),
                alt.value('green')
            )
        ).properties(
            title='Daily Schedule Adherence (%)'
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        # Teacher's weekly notes
        st.write("### Teacher's Notes")
        teacher_notes = week_data.get('teacher_notes', '')
        
        if not teacher_notes:
            st.info("No teacher notes available for this week")
        else:
            st.write(teacher_notes)
    else:
        st.info("No data available for the selected week")

def render_feedback_form(state, child_data):
    """Render feedback form for parents to provide input on their child's progress."""
    st.subheader("Provide Feedback")
    
    # Tabs for different types of feedback
    feedback_tab1, feedback_tab2, feedback_tab3 = st.tabs([
        "Weekly Feedback",
        "Roadmap Adjustments",
        "Observation Notes"
    ])
    
    with feedback_tab1:
        st.write("### Weekly Progress Feedback")
        st.write("Share your observations about your child's progress this week. This helps tailor the roadmap to better fit their needs.")
        
        with st.form("weekly_feedback"):
            # Overall satisfaction
            satisfaction = st.slider(
                "Overall satisfaction with this week's progress",
                1, 5, 3
            )
            
            # Study environment assessment
            study_environment = st.selectbox(
                "How would you rate your child's study environment this week?",
                ["Very Conducive", "Adequate", "Some Distractions", "Highly Distracting"]
            )
            
            # Time management assessment
            time_management = st.selectbox(
                "How well did your child manage their study time?",
                ["Excellent", "Good", "Adequate", "Needs Improvement", "Poor"]
            )
            
            # Stress level assessment
            stress_level = st.selectbox(
                "What was your child's stress level this week?",
                ["No Stress", "Low Stress", "Moderate Stress", "High Stress", "Extreme Stress"]
            )
            
            # External factors
            external_factors = st.multiselect(
                "Were there any external factors affecting your child's studies?",
                ["Family Events", "Health Issues", "Extracurricular Activities", "Social Events", "Technology Distractions", "Other"]
            )
            
            if "Other" in external_factors:
                other_factors = st.text_input("Please specify other factors")
            
            # Additional observations
            additional_observations = st.text_area(
                "Additional observations or concerns"
            )
            
            # Submit button
            submit_weekly = st.form_submit_button("Submit Weekly Feedback")
            if submit_weekly:
                st.success("Thank you for your feedback! It will help us adjust your child's roadmap accordingly.")
    
    with feedback_tab2:
        st.write("### Roadmap Adjustment Requests")
        st.write("Request specific changes to your child's study roadmap based on your observations.")
        
        with st.form("roadmap_adjustments"):
            # Adjustment type
            adjustment_type = st.radio(
                "Type of adjustment needed",
                ["Study Load", "Topic Focus", "Schedule Timing", "Resources", "Other"]
            )
            
            # Specific details based on adjustment type
            if adjustment_type == "Study Load":
                load_change = st.radio(
                    "Study load adjustment",
                    ["Reduce Load", "Increase Load", "Redistribute Load"]
                )
                load_reason = st.text_area("Reason for load adjustment")
                
            elif adjustment_type == "Topic Focus":
                focus_change = st.text_area("Which topics need more or less focus?")
                
            elif adjustment_type == "Schedule Timing":
                timing_change = st.text_area("What schedule changes would be beneficial?")
                
            elif adjustment_type == "Resources":
                resource_feedback = st.text_area("Feedback on current resources or suggestions for new ones")
                
            else:  # Other
                other_adjustment = st.text_area("Please describe the needed adjustment")
            
            # Urgency level
            urgency = st.selectbox(
                "Urgency of this adjustment",
                ["Low - Can be implemented gradually", "Medium - Implement in next update", "High - Needs immediate attention"]
            )
            
            # Submit button
            submit_adjustment = st.form_submit_button("Submit Adjustment Request")
            if submit_adjustment:
                st.success("Your adjustment request has been submitted and will be reviewed by the teacher and AI system.")
    
    with feedback_tab3:
        st.write("### Observation Notes")
        st.write("Record specific observations about your child's study habits, challenges, or achievements.")
        
        with st.form("observation_notes"):
            # Observation date
            observation_date = st.date_input(
                "Date of observation",
                datetime.now()
            )
            
            # Observation category
            observation_category = st.selectbox(
                "Category",
                ["Study Habits", "Learning Style", "Motivation Level", "Comprehension", "Test Performance", "Other"]
            )
            
            # Observation details
            observation_details = st.text_area(
                "Detailed observation"
            )
            
            # Impact on studies
            impact = st.selectbox(
                "Impact on studies",
                ["Positive", "Neutral", "Negative"]
            )
            
            # Suggested action
            suggested_action = st.text_area(
                "Suggested action (if any)"
            )
            
            # Submit button
            submit_observation = st.form_submit_button("Submit Observation")
            if submit_observation:
                st.success("Your observation has been recorded and will be used to improve your child's learning experience.")

def render_communication_hub(state, child_data):
    """Render communication hub for parent-teacher interaction."""
    st.subheader("Communication Hub")
    
    # Display tabs for different communication channels
    comm_tab1, comm_tab2, comm_tab3 = st.tabs([
        "Message Teacher",
        "Recent Communications",
        "Scheduled Meetings"
    ])
    
    with comm_tab1:
        st.write("### Message Teacher")
        
        # Get teacher information
        teachers = state.parent_data.get('teachers', [])
        
        if not teachers:
            st.info("No teacher information available")
        else:
            # Teacher selection
            selected_teacher = st.selectbox(
                "Select Teacher",
                [f"{teacher.get('name', '')} ({teacher.get('subject', '')})" for teacher in teachers]
            )
            
            # Message type
            message_type = st.selectbox(
                "Message Category",
                ["General Inquiry", "Progress Concern", "Schedule Request", "Resource Question", "Other"]
            )
            
            # Message content
            message = st.text_area(
                "Your Message"
            )
            
            # Attachments
            has_attachment = st.checkbox("Include Attachment")
            if has_attachment:
                attachment = st.file_uploader("Upload file", type=["pdf", "doc", "docx", "jpg", "png"])
            
            # Send button
            if st.button("Send Message"):
                st.success("Your message has been sent. You'll receive a notification when the teacher responds.")
    
    with comm_tab2:
        st.write("### Recent Communications")
        
        # Display message history
        messages = state.parent_data.get('message_history', [])
        
        if not messages:
            st.info("No recent communications")
        else:
            for message in messages:
                with st.container():
                    # Message container styling based on sender
                    is_sent = message.get('sender_type', '') == 'parent'
                    
                    if is_sent:
                        st.write("**You**")
                    else:
                        st.write(f"**{message.get('sender', 'Teacher')}**")
                    
                    # Display message
                    if is_sent:
                        st.success(message.get('content', ''))
                    else:
                        st.info(message.get('content', ''))
                    
                    # Show timestamp
                    st.caption(f"{message.get('timestamp', '')}")
                    
                    # Display attachments if any
                    attachments = message.get('attachments', [])
                    if attachments:
                        st.write("**Attachments:**")
                        for attachment in attachments:
                            st.write(f"- {attachment.get('name', '')}")
                    
                    st.divider()
            
            # Quick reply
            quick_reply = st.text_area("Quick Reply")
            if st.button("Send Reply"):
                st.success("Reply sent!")
    
    with comm_tab3:
        st.write("### Scheduled Meetings")
        
        # Display upcoming meetings
        meetings = state.parent_data.get('scheduled_meetings', [])
        
        if not meetings:
            st.info("No meetings scheduled")
        else:
            for meeting in meetings:
                with st.expander(f"{meeting.get('title', '')} - {meeting.get('date', '')}"):
                    st.write(f"**Time:** {meeting.get('time', '')}")
                    st.write(f"**With:** {meeting.get('with', '')}")
                    st.write(f"**Purpose:** {meeting.get('purpose', '')}")
                    
                    # Meeting link if virtual
                    if meeting.get('type', '') == 'virtual':
                        st.write(f"**Meeting Link:** {meeting.get('link', 'Link will be available 15 minutes before the meeting')}")
                    else:
                        st.write(f"**Location:** {meeting.get('location', '')}")
                    
                    # Add to calendar option
                    st.download_button(
                        "Add to Calendar",
                        "Calendar data would go here",
                        file_name=f"{meeting.get('title', 'meeting')}.ics",
                        mime="text/calendar"
                    )
                    
                    # Reschedule option
                    if st.button("Request Reschedule", key=f"reschedule_{meeting.get('id', '')}"):
                        st.session_state[f"show_reschedule_{meeting.get('id', '')}"] = True
                    
                    # Show reschedule form if requested
                    if st.session_state.get(f"show_reschedule_{meeting.get('id', '')}", False):
                        with st.form(f"reschedule_form_{meeting.get('id', '')}"):
                            st.write("**Reschedule Request**")
                            new_date = st.date_input("Preferred Date")
                            new_time = st.selectbox("Preferred Time", ["Morning", "Afternoon", "Evening"])
                            reason = st.text_area("Reason for Rescheduling")
                            
                            submit_reschedule = st.form_submit_button("Submit Reschedule Request")
                            if submit_reschedule:
                                st.success("Your reschedule request has been submitted.")
                                st.session_state[f"show_reschedule_{meeting.get('id', '')}"] = False
        
        # Schedule new meeting
        st.write("### Schedule New Meeting")
        with st.form("schedule_meeting"):
            meeting_purpose = st.selectbox(
                "Meeting Purpose",
                ["Progress Review", "Specific Concern", "Roadmap Discussion", "General Check-in", "Other"]
            )
            
            preferred_date = st.date_input(
                "Preferred Date",
                min_value=datetime.now().date()
            )
            
            preferred_time = st.selectbox(
                "Preferred Time",
                ["Morning (9AM-12PM)", "Afternoon (1PM-4PM)", "Evening (5PM-7PM)"]
            )
            
            meeting_type = st.radio(
                "Meeting Type",
                ["Virtual", "In-Person"]
            )
            
            specific_topics = st.text_area(
                "Specific Topics to Discuss"
            )
            
            submit_meeting = st.form_submit_button("Request Meeting")
            if submit_meeting:
                st.success("Your meeting request has been submitted. You'll receive a confirmation once it's scheduled.")