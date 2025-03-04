import streamlit as st
import os
from dotenv import load_dotenv
from agents.roadmap_agent import RoadmapAgent
from agents.monitor_agent import MonitorAgent
from agents.feedback_agent import FeedbackAgent
from components.student_view import render_student_view
from components.teacher_view import render_teacher_view
from components.parent_view import render_parent_view
from utils.state import initialize_session_state, save_state, load_state
from utils.data_models import StudentData, ProgressData, FeedbackData

# Load environment variables
load_dotenv()

def main():
    # Set up page configuration
    st.set_page_config(
        page_title="Roadmap AI System",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Display header
    st.title("Roadmap AI System")
    st.markdown("### Personalized Learning Roadmaps with AI-powered Feedback")
    
    # Sidebar for navigation and settings
    with st.sidebar:
        st.header("Navigation")
        user_role = st.radio(
            "Select User Role:",
            ["Student", "Teacher", "Parent"]
        )
        
        st.header("Settings")
        model_selection = st.selectbox(
            "AI Model:",
            ["llama3-70b-8192", "mixtral-8x7b", "gemma-7b"],
            index=0
        )
        
        # Initialize agents if not already in session state
        if "roadmap_agent" not in st.session_state:
            st.session_state.roadmap_agent = RoadmapAgent(model_name=model_selection)
            st.session_state.monitor_agent = MonitorAgent(model_name=model_selection)
            st.session_state.feedback_agent = FeedbackAgent(model_name=model_selection)
        
        # Display API status
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            st.success("API Connected ✓")
        else:
            st.error("API Key Missing! Check .env file")
    
    # Main content area based on selected role
    if user_role == "Student":
        display_student_view()
    elif user_role == "Teacher":
        display_teacher_view()
    else:  # Parent view
        display_parent_view()
    
    # Footer
    st.markdown("---")
    st.caption("Roadmap AI System v1.0 | Powered by Groq LLMs")

def display_student_view():
    """Display the student dashboard"""
    import streamlit as st
    
    # Import rendering functions
    from render_functions import (
        render_student_view,
        render_daily_plan,
        render_weekly_roadmap,
        render_performance_metrics,
        render_swot_analysis
    )
    
    # Initialize roadmap_agent if not already done
    if "roadmap_agent" not in st.session_state:
        from agents.roadmap_agent import RoadmapAgent
        st.session_state.roadmap_agent = RoadmapAgent()
    
    if "monitor_agent" not in st.session_state:
        from agents.monitor_agent import MonitorAgent
        st.session_state.monitor_agent = MonitorAgent()
    
    # Tabs for different student functions
    tab1, tab2, tab3 = st.tabs(["My Roadmap", "Progress Tracking", "Resources"])
    
    with tab1:
        st.header("My Learning Roadmap")
        
        # Student information input
        with st.expander("My Information", expanded=False):
            if st.button("Use Sample Data"):
                # Load sample student data
                from data.sample_data import get_sample_student_data
                st.session_state.student_data = get_sample_student_data()
                # Reload the page to ensure the UI updates
                st.rerun()
            else:
                # Form for student data input
                with st.form("student_info_form"):
                    name = st.text_input("Name", value=st.session_state.get("name", ""))
                    grade = st.text_input("Grade/Year", value=st.session_state.get("grade", ""))
                    subjects = st.multiselect(
                        "Subjects",
                        ["Math", "Science","Biology", "Chemistry", "Other"],
                        default=st.session_state.get("subjects", [])
                    )
                    
                    # Current performance
                    st.subheader("Current Performance")
                    performance = st.text_area(
                        "Describe your current academic performance", 
                        value=st.session_state.get("performance", "")
                    )
                    
                    # Goals
                    st.subheader("Goals")
                    goals = st.text_area(
                        "What are your academic goals?", 
                        value=st.session_state.get("goals", "")
                    )
                    
                    # Strengths and weaknesses
                    col1, col2 = st.columns(2)
                    with col1:
                        strengths = st.text_area(
                            "What are your strengths?", 
                            value=st.session_state.get("strengths", "")
                        )
                    with col2:
                        weaknesses = st.text_area(
                            "What areas need improvement?", 
                            value=st.session_state.get("weaknesses", "")
                        )
                    
                    submit = st.form_submit_button("Save Information")
                    
                    if submit:
                        # Save to session state
                        st.session_state.student_data = {
                            "name": name,
                            "grade": grade,
                            "subjects": subjects,  # Store as a list, not a joined string
                            "performance": performance,
                            "goals": goals,
                            "strengths": strengths,
                            "weaknesses": weaknesses
                        }
                        st.success("Information saved!")
        
        # Generate roadmap
        if "student_data" in st.session_state:
            # Add a check to display the current student data (for debugging)
            with st.expander("Student Data (Debug)"):
                st.write(st.session_state.student_data)
            
            # Generate roadmap button
            generate_roadmap = st.button("Generate My Roadmap")
            
            # Check if roadmap should be displayed
            if generate_roadmap or "roadmap" in st.session_state:
                with st.spinner("Creating your personalized roadmap..."):
                    try:
                        if generate_roadmap or "roadmap" not in st.session_state:
                            # Generate new roadmap
                            roadmap = st.session_state.roadmap_agent.generate_roadmap(
                                st.session_state.student_data
                            )
                            st.session_state.roadmap = roadmap
                    except Exception as e:
                        st.error(f"Error generating roadmap: {str(e)}")
                
                # Display the roadmap
                if "roadmap" in st.session_state:
                    st.markdown("## Your Personalized Roadmap")
                    st.markdown(st.session_state.roadmap)
                    
                    # Allow roadmap to be refreshed
                    if st.button("Regenerate Roadmap"):
                        # Remove the roadmap from session state
                        if "roadmap" in st.session_state:
                            del st.session_state.roadmap
                        st.rerun()
        else:
            st.info("Please enter your information to generate a roadmap.")
    
    with tab2:
        st.header("Track Your Progress")
        
        # Only show if roadmap exists
        if "roadmap" in st.session_state:
            # Progress tracking form
            with st.form("progress_tracking"):
                st.subheader("Update Your Progress")
                
                # Task completion
                completed_tasks = st.text_area(
                    "What tasks have you completed from your roadmap?",
                    placeholder="List the specific tasks you've completed..."
                )
                
                # Time tracking
                time_spent = st.text_area(
                    "How much time have you spent studying each subject?",
                    placeholder="Math: 4 hours\nScience: 3 hours\n..."
                )
                
                # Assessment results
                assessment_results = st.text_area(
                    "Enter any assessment results or practice scores",
                    placeholder="Quiz 1: 85%\nPractice Test: 78%\n..."
                )
                
                submit_progress = st.form_submit_button("Submit Progress Update")
                
                if submit_progress:
                    # Store progress data
                    st.session_state.progress_data = {
                        "completed_tasks": completed_tasks,
                        "time_spent": time_spent,
                        "assessment_results": assessment_results
                    }
                    
                    # Generate progress analysis
                    with st.spinner("Analyzing your progress..."):
                        progress_analysis = st.session_state.monitor_agent.analyze_progress(
                            st.session_state.roadmap,
                            completed_tasks,
                            time_spent,
                            assessment_results
                        )
                        st.session_state.progress_analysis = progress_analysis
                    
                    st.success("Progress updated!")
            
            # Display progress analysis if available
            if "progress_analysis" in st.session_state:
                st.markdown("## Progress Analysis")
                st.markdown(st.session_state.progress_analysis)
                
                # Option to update roadmap based on progress
                if st.button("Update My Roadmap Based on Progress"):
                    with st.spinner("Updating your roadmap..."):
                        updated_roadmap = st.session_state.roadmap_agent.update_roadmap(
                            st.session_state.roadmap,
                            st.session_state.progress_data,
                            "Student self-reported progress"
                        )
                        st.session_state.roadmap = updated_roadmap
                    
                    st.success("Roadmap updated!")
                    st.rerun()
        else:
            st.info("Generate a roadmap first to track your progress.")
    
    with tab3:
        st.header("Learning Resources")
        
        # Check if student data and roadmap exist
        if "student_data" in st.session_state and "roadmap" in st.session_state:
            # Create the tabs that were missing
            resource_tabs = st.tabs(["Daily Plan", "Weekly Roadmap", "Performance", "SWOT Analysis"])
            
            with resource_tabs[0]:  # Daily Plan
                render_daily_plan(st.session_state)
            
            with resource_tabs[1]:  # Weekly Roadmap
                render_weekly_roadmap(st.session_state)
            
            with resource_tabs[2]:  # Performance
                render_performance_metrics(st.session_state)
            
            with resource_tabs[3]:  # SWOT Analysis
                render_swot_analysis(st.session_state)
        else:
            st.info("Please generate a roadmap first to view your resources and detailed plans.")

def display_teacher_view():
    """Display the teacher dashboard"""
    import streamlit as st
    
    st.header("Teacher Dashboard")
    
    # Initialize a list to store registered students if not already done
    if "registered_students" not in st.session_state:
        st.session_state.registered_students = []
    
    # Check if a new student has registered and add them to the list
    if "student_data" in st.session_state and "name" in st.session_state.student_data:
        student_name = st.session_state.student_data["name"]
        if student_name and student_name not in st.session_state.registered_students:
            st.session_state.registered_students.append(student_name)
    
    # Display dynamic student list
    if st.session_state.registered_students:
        selected_student = st.selectbox(
            "Select Student", 
            st.session_state.registered_students
        )
        
        # Display current student roadmap if available
        if "roadmap" in st.session_state:
            st.subheader(f"{selected_student}'s Current Roadmap")
            st.markdown(st.session_state.roadmap)
            
            # Teacher feedback form
            with st.form("teacher_feedback_form"):
                st.subheader("Provide Feedback")
                teacher_feedback = st.text_area(
                    "Enter your feedback on the student's roadmap and progress",
                    placeholder="Share your observations, suggestions, and concerns...",
                    key="feedback_text_input"
                )
                
                submit_feedback = st.form_submit_button("Submit Feedback")
                
                if submit_feedback and teacher_feedback:  # Added check for non-empty feedback
                    with st.spinner("Processing feedback..."):
                        # Initialize feedback_agent if not already done
                        if "feedback_agent" not in st.session_state:
                            from agents.feedback_agent import FeedbackAgent
                            st.session_state.feedback_agent = FeedbackAgent()
                        
                        try:
                            feedback_response = st.session_state.feedback_agent.process_teacher_feedback(
                                st.session_state.roadmap,
                                teacher_feedback
                            )
                            # Store feedback and response
                            st.session_state.teacher_feedback_data = teacher_feedback
                            st.session_state.feedback_response = feedback_response
                            st.success("Feedback submitted!")
                        except Exception as e:
                            st.error(f"Error processing feedback: {str(e)}")
            
            # Display feedback analysis if available - moved outside the form
            if "feedback_response" in st.session_state and st.session_state.feedback_response:
                st.markdown("## Feedback Analysis")
                st.markdown(st.session_state.feedback_response)
                
                # Option to update roadmap based on feedback
                if st.button("Update Roadmap Based on Feedback"):
                    with st.spinner("Updating roadmap..."):
                        # Initialize roadmap_agent if not already done
                        if "roadmap_agent" not in st.session_state:
                            from agents.roadmap_agent import RoadmapAgent
                            st.session_state.roadmap_agent = RoadmapAgent()
                        
                        updated_roadmap = st.session_state.roadmap_agent.update_roadmap(
                            st.session_state.roadmap,
                            {},  # No progress data in this case
                            st.session_state.teacher_feedback_data
                        )
                        st.session_state.roadmap = updated_roadmap
                    
                    st.success("Roadmap updated based on feedback!")
                    st.rerun()
        else:
            st.info(f"No roadmap available for {selected_student} yet.")
    else:
        st.info("No students have registered yet. Students will appear here once they've entered their information.")
    
    # Additional teacher tools
    if 'teacher_data' not in st.session_state:
        st.session_state.teacher_data = {
            'name': 'Teacher',
        }
    
    # Make sure render_teacher_view is imported or defined
    render_teacher_view(st.session_state)

def display_parent_view():
    """Display the parent dashboard"""
    st.header("Parent Dashboard")
    if 'parent_data' not in st.session_state:
        st.session_state.parent_data = {}
    
    # Child selection for parents with multiple children
    child_list = ["Alex Johnson", "Jamie Smith"]
    selected_child = st.selectbox("Select Child", child_list)
    
    # Display current child roadmap if available
    if "roadmap" in st.session_state:
        st.subheader(f"{selected_child}'s Current Roadmap")
        st.markdown(st.session_state.roadmap)
        
        # Parent feedback form
        with st.form("parent_feedback"):
            st.subheader("Provide Feedback")
            parent_feedback = st.text_area(
                "Enter your feedback on your child's roadmap and progress",
                placeholder="Share your observations, home context, and concerns..."
            )
            
            submit_feedback = st.form_submit_button("Submit Feedback")
            
            if submit_feedback:
                with st.spinner("Processing feedback..."):
                    feedback_response = st.session_state.feedback_agent.process_parent_feedback(
                        st.session_state.roadmap,
                        parent_feedback
                    )
                    st.session_state["parent_feedback"] = parent_feedback
                    st.session_state["parent_response"] = feedback_response
                
                st.success("Feedback submitted!")
        
        # Display feedback analysis if available
        if "parent_response" in st.session_state:
            st.markdown("## Feedback Analysis")
            st.markdown(st.session_state.parent_response)
            
            # Option to reconcile feedback if both teacher and parent feedback exist
            if "teacher_feedback" in st.session_state and "parent_feedback" in st.session_state:
                if st.button("Reconcile All Feedback"):
                    with st.spinner("Reconciling feedback from all sources..."):
                        student_input = st.session_state.progress_data.get("completed_tasks", "No student input available")
                        reconciled_feedback = st.session_state.feedback_agent.reconcile_feedback(
                            st.session_state.teacher_feedback,
                            st.session_state.parent_feedback,
                            student_input
                        )
                        st.session_state.reconciled_feedback = reconciled_feedback
                    
                    st.success("Feedback reconciled!")
            
            # Display reconciled feedback if available
            if "reconciled_feedback" in st.session_state:
                st.markdown("## Reconciled Feedback")
                st.markdown(st.session_state.reconciled_feedback)
                
                # Update roadmap based on reconciled feedback
                if st.button("Update Roadmap Based on Reconciled Feedback"):
                    with st.spinner("Updating roadmap..."):
                        updated_roadmap = st.session_state.roadmap_agent.update_roadmap(
                            st.session_state.roadmap,
                            st.session_state.progress_data if "progress_data" in st.session_state else {},
                            st.session_state.reconciled_feedback
                        )
                        st.session_state.roadmap = updated_roadmap
                    
                    st.success("Roadmap updated based on reconciled feedback!")
                    st.experimental_rerun()
    else:
        st.info("No roadmap available for your child yet.")
    
    # Additional parent tools
    render_parent_view(st.session_state)

if __name__ == "__main__":
    main()