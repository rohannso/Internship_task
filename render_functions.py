import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import altair as alt

def render_student_view(state):
    """Render the student dashboard view with personalized roadmap and progress tracking."""
    st.title("My Study Roadmap")
    
    # Student Profile Section
    with st.expander("My Profile", expanded=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://via.placeholder.com/150", width=150)
        with col2:
            st.subheader(f"{state.student_data.get('name', 'Student')}")
            st.write(f"Target Exam: {state.student_data.get('target_exam', 'JEE/NEET')}")
            st.write(f"Target Score: {state.student_data.get('target_score', 'Not set')}")
            
            # Display current week's progress
            current_progress = state.student_data.get('current_progress', 0)
            st.progress(current_progress/100)
            st.caption(f"Current Week Progress: {current_progress}%")
    
    # SWOT Analysis Tab
    tab1, tab2, tab3, tab4 = st.tabs(["Daily Plan", "Weekly Roadmap", "Performance", "SWOT Analysis"])
    
    with tab1:
        render_daily_plan(state)
        
    with tab2:
        render_weekly_roadmap(state)
        
    with tab3:
        render_performance_metrics(state)
        
    with tab4:
        render_swot_analysis(state)
    
    # Notifications and Reminders
    with st.sidebar:
        st.subheader("Notifications")
        for notification in state.student_data.get('notifications', []):
            with st.container():
                st.info(notification.get('message', ''))
                st.caption(notification.get('time', 'Today'))
        
        st.subheader("Upcoming Deadlines")
        for deadline in state.student_data.get('upcoming_deadlines', []):
            days_left = (datetime.strptime(deadline.get('date', '2025-03-10'), '%Y-%m-%d') - datetime.now()).days
            with st.container():
                st.warning(f"{deadline.get('title', '')}: {days_left} days left")

def render_daily_plan(state):
    """Render today's study plan."""
    st.subheader("Today's Study Plan")
    
    # Today's date
    today = datetime.now().strftime("%A, %B %d, %Y")
    st.write(f"**{today}**")
    
    # Get today's tasks
    today_tasks = state.student_data.get('daily_tasks', [])
    
    if not today_tasks:
        st.info("No tasks scheduled for today. Take some time to review your past materials.")
        return
    
    # Morning, Afternoon, Evening sections
    time_sections = {
        "Morning": [task for task in today_tasks if task.get('time_slot') == 'morning'],
        "Afternoon": [task for task in today_tasks if task.get('time_slot') == 'afternoon'],
        "Evening": [task for task in today_tasks if task.get('time_slot') == 'evening']
    }
    
    for section, tasks in time_sections.items():
        st.write(f"#### {section}")
        if not tasks:
            st.write("No tasks scheduled")
            continue
            
        for i, task in enumerate(tasks):
            col1, col2, col3 = st.columns([5, 3, 2])
            with col1:
                st.checkbox(
                    task.get('title', f'Task {i+1}'),
                    value=task.get('completed', False),
                    key=f"task_{task.get('id', i)}"
                )
            with col2:
                st.write(f"{task.get('start_time', '')} - {task.get('end_time', '')}")
            with col3:
                st.write(f"{task.get('subject', '')}")
            
            # Task details in expandable section
            with st.expander("Details"):
                st.write(task.get('description', 'No details available'))
                
                # Show resources
                if task.get('resources', []):
                    st.write("**Resources:**")
                    for resource in task.get('resources', []):
                        st.markdown(f"- [{resource.get('title', 'Resource')}]({resource.get('url', '#')})")
                
                # Show related topics/concepts
                if task.get('related_topics', []):
                    st.write("**Related Topics:**")
                    st.write(", ".join(task.get('related_topics', [])))
    
    # Add quick actions
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Request Schedule Change", key="request_schedule_change"):
            st.session_state.show_reschedule_form = True
            
    with col2:
        if st.button("Mark All Complete", key="mark_all_complete"):
            st.success("All tasks marked as complete!")
    
    # Show reschedule form if requested
    if st.session_state.get('show_reschedule_form', False):
        with st.form("reschedule_form"):
            st.write("**Request Schedule Adjustment**")
            task_to_reschedule = st.selectbox(
                "Select task to reschedule:",
                [task.get('title', f'Task {i+1}') for i, task in enumerate(today_tasks)]
            )
            reason = st.text_area("Reason for rescheduling:")
            preferred_time = st.selectbox(
                "Preferred time slot:",
                ["Morning", "Afternoon", "Evening", "Tomorrow"]
            )
            
            submitted = st.form_submit_button("Submit Request")
            if submitted:
                st.success("Your request has been submitted and will be reviewed!")
                st.session_state.show_reschedule_form = False

def render_weekly_roadmap(state):
    """Render weekly roadmap with subject distribution."""
    st.subheader("Weekly Study Roadmap")
    
    # Get the current week's data
    current_week = state.student_data.get('current_week', 1)
    weeks_data = state.student_data.get('weeks_data', [])
    
    if not weeks_data:
        st.info("No weekly roadmap data available. Please complete your profile to generate a detailed roadmap.")
        return
    
    # Week selection
    selected_week = st.selectbox(
        "Select Week:", 
        range(1, len(weeks_data) + 1),
        index=current_week - 1,
        key="week_selector"
    )
    
    # Display weekly plan
    week_data = weeks_data[selected_week - 1] if selected_week <= len(weeks_data) else {}
    
    # Weekly subject distribution pie chart
    subject_hours = week_data.get('subject_hours', {})
    if subject_hours:
        fig = px.pie(
            names=list(subject_hours.keys()),
            values=list(subject_hours.values()),
            title="Study Hours Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Weekly calendar view
    st.write("### Weekly Calendar")
    
    # Create weekly calendar dataframe
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    time_slots = ["Morning", "Afternoon", "Evening"]
    
    # Get weekly schedule
    weekly_schedule = week_data.get('schedule', {})
    
    # Create a calendar view
    for day in days:
        with st.expander(day):
            for slot in time_slots:
                st.write(f"**{slot}**")
                day_tasks = weekly_schedule.get(day, {}).get(slot, [])
                
                if not day_tasks:
                    st.write("No tasks scheduled")
                    continue
                
                for task in day_tasks:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"{task.get('title', 'Task')}")
                    with col2:
                        st.write(f"{task.get('subject', '')}")
    
    # Weekly focus areas and goals
    st.write("### Weekly Focus Areas")
    focus_areas = week_data.get('focus_areas', [])
    for area in focus_areas:
        st.write(f"- **{area.get('subject', '')}**: {area.get('topic', '')}")
    
    # Weekly assessment plan
    st.write("### Assessments This Week")
    assessments = week_data.get('assessments', [])
    for assessment in assessments:
        st.write(f"- **{assessment.get('title', '')}** ({assessment.get('day', '')}): {assessment.get('description', '')}")

def render_performance_metrics(state):
    """Render performance metrics and analytics."""
    st.subheader("My Performance Analytics")
    
    if not state.student_data.get('subjects', []):
        st.info("No performance data available. Please complete assessments to view your performance metrics.")
        return
    
    # Overall subject performance
    subjects = state.student_data.get('subjects', [])
    subject_scores = {}
    for i, subject in enumerate(subjects):
        if isinstance(subject, dict):
            subject_scores[subject.get('name', f'Subject {i}')] = subject.get('score', 0)
        elif isinstance(subject, str):
            subject_scores[subject] = 0
    
    # Create bar chart for subject performance
    if subject_scores:
        subject_df = pd.DataFrame({
            'Subject': list(subject_scores.keys()),
            'Score': list(subject_scores.values())
        })
        
        chart = alt.Chart(subject_df).mark_bar().encode(
            x=alt.X('Subject', sort=None),
            y='Score',
            color=alt.Color('Subject', legend=None)
        ).properties(
            title='Subject Performance'
        )
        
        st.altair_chart(chart, use_container_width=True)
    
    # Progress over time
    st.write("### Progress Over Time")
    
    # Get historical performance data
    history = state.student_data.get('performance_history', [])
    if history:
        history_df = pd.DataFrame(history)
        
        # Line chart for progress over time
        progress_chart = alt.Chart(history_df).mark_line(point=True).encode(
            x='week:O',
            y='average_score',
            tooltip=['week', 'average_score']
        ).properties(
            title='Weekly Average Score'
        )
        
        st.altair_chart(progress_chart, use_container_width=True)
    else:
        st.info("No historical performance data available yet.")
    
    # Topic-wise performance
    st.write("### Topic Performance")
    
    # Create tabs for each subject - Fixed to handle both string and dict types
    if subjects:
        # Create tab labels that work for both string and dictionary subjects
        tab_labels = []
        for i, subject in enumerate(subjects):
            if isinstance(subject, dict):
                tab_labels.append(subject.get('name', f'Subject {i}'))
            else:
                tab_labels.append(subject)
        
        if tab_labels:
            subject_tabs = st.tabs(tab_labels)
            
            for i, tab in enumerate(subject_tabs):
                with tab:
                    subject_data = subjects[i]
                    
                    # Handle subject data differently based on type
                    if isinstance(subject_data, dict):
                        # Get topics for this subject
                        topics = subject_data.get('topics', [])
                        
                        if not topics:
                            st.info(f"No topic data available for {subject_data.get('name', 'this subject')}")
                            continue
                        
                        # Create topic performance dataframe
                        topic_df = pd.DataFrame({
                            'Topic': [topic.get('name', f'Topic {j}') for j, topic in enumerate(topics)],
                            'Score': [topic.get('score', 0) for topic in topics],
                            'Mastery': [topic.get('mastery', 'Low') for topic in topics]
                        })
                        
                        # Display topic performance
                        st.dataframe(topic_df, use_container_width=True)
                        
                        # Highlight areas for improvement
                        weak_topics = [topic for topic in topics if topic.get('score', 0) < 70]
                        if weak_topics:
                            st.write("### Areas for Improvement")
                            for topic in weak_topics:
                                st.write(f"- {topic.get('name', 'Topic')}: {topic.get('recommendation', 'Focus on this topic')}")
                    else:
                        # Handle string subjects
                        st.info(f"No detailed data available for {subject_data}")

def render_swot_analysis(state):
    """Render SWOT analysis for the student."""
    st.subheader("My SWOT Analysis")
    
    swot = state.student_data.get('swot', {})
    
    if not swot:
        st.info("SWOT analysis not available. Please complete your profile to generate a SWOT analysis.")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Strengths")
        strengths = swot.get('strengths', [])
        for strength in strengths:
            st.success(f"- {strength}")
            
        st.write("### Weaknesses")
        weaknesses = swot.get('weaknesses', [])
        for weakness in weaknesses:
            st.error(f"- {weakness}")
    
    with col2:
        st.write("### Opportunities")
        opportunities = swot.get('opportunities', [])
        for opportunity in opportunities:
            st.info(f"- {opportunity}")
            
        st.write("### Threats")
        threats = swot.get('threats', [])
        for threat in threats:
            st.warning(f"- {threat}")
    
    # Action plan based on SWOT
    st.write("### Recommended Action Plan")
    action_plan = swot.get('action_plan', [])
    for action in action_plan:
        st.write(f"- **{action.get('title', '')}**: {action.get('description', '')}")