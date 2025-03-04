import streamlit as st
import json
import os
from datetime import datetime
import uuid
from utils.data_models import Student, Roadmap, Progress, Feedback

class SessionState:
    """Helper class for managing session state across different pages"""
    
    @staticmethod
    def get_current_user():
        """Get current user information"""
        if 'user' not in st.session_state:
            st.session_state.user = {
                'id': None,
                'name': None,
                'role': None,
                'is_authenticated': False
            }
        return st.session_state.user
    
    @staticmethod
    def set_current_user(id, name, role):
        """Set current user information"""
        st.session_state.user = {
            'id': id,
            'name': name,
            'role': role,
            'is_authenticated': True
        }
    
    @staticmethod
    def is_authenticated():
        """Check if user is authenticated"""
        return st.session_state.get('user', {}).get('is_authenticated', False)
    
    @staticmethod
    def logout():
        """Log out current user"""
        if 'user' in st.session_state:
            st.session_state.user = {
                'id': None,
                'name': None,
                'role': None,
                'is_authenticated': False
            }


class DataStore:
    """Simple data storage using files (for MVP without database)"""
    
    @staticmethod
    def _ensure_data_dir():
        """Ensure data directory exists"""
        if not os.path.exists('data/storage'):
            os.makedirs('data/storage', exist_ok=True)
    
    @staticmethod
    def save_student(student):
        """Save student data"""
        DataStore._ensure_data_dir()
        
        if not isinstance(student, Student):
            student = Student.from_dict(student)
            
        if not student.id:
            student.id = str(uuid.uuid4())
            
        file_path = f'data/storage/student_{student.id}.json'
        
        with open(file_path, 'w') as f:
            json.dump(student.to_dict(), f, indent=2)
            
        return student.id
    
    @staticmethod
    def get_student(student_id):
        """Get student data"""
        file_path = f'data/storage/student_{student_id}.json'
        
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        return Student.from_dict(data)
    
    @staticmethod
    def save_roadmap(roadmap):
        """Save roadmap data"""
        DataStore._ensure_data_dir()
        
        if not isinstance(roadmap, Roadmap):
            roadmap = Roadmap.from_dict(roadmap)
            
        if not roadmap.id:
            roadmap.id = str(uuid.uuid4())
            
        roadmap.updated_at = datetime.now()
            
        file_path = f'data/storage/roadmap_{roadmap.id}.json'
        
        with open(file_path, 'w') as f:
            json.dump(roadmap.to_dict(), f, indent=2)
            
        return roadmap.id
    
    @staticmethod
    def get_roadmap(roadmap_id):
        """Get roadmap data"""
        file_path = f'data/storage/roadmap_{roadmap_id}.json'
        
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        return Roadmap.from_dict(data)
    
    @staticmethod
    def get_student_roadmap(student_id):
        """Get the latest roadmap for a student"""
        # This is inefficient but works for MVP
        data_dir = 'data/storage'
        
        if not os.path.exists(data_dir):
            return None
            
        roadmaps = []
        
        for filename in os.listdir(data_dir):
            if filename.startswith('roadmap_') and filename.endswith('.json'):
                file_path = os.path.join(data_dir, filename)
                
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                if data.get('student_id') == student_id:
                    roadmaps.append(Roadmap.from_dict(data))
        
        if not roadmaps:
            return None
            
        # Return the most recent roadmap
        return sorted(roadmaps, key=lambda r: r.updated_at, reverse=True)[0]
    
    @staticmethod
    def save_progress(progress):
        """Save progress data"""
        DataStore._ensure_data_dir()
        
        if not isinstance(progress, Progress):
            progress = Progress.from_dict(progress)
            
        if not progress.id:
            progress.id = str(uuid.uuid4())
            
        progress.updated_at = datetime.now()
            
        file_path = f'data/storage/progress_{progress.id}.json'
        
        with open(file_path, 'w') as f:
            json.dump(progress.to_dict(), f, indent=2)
            
        return progress.id
    
    @staticmethod
    def get_progress(progress_id):
        """Get progress data"""
        file_path = f'data/storage/progress_{progress_id}.json'
        
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        return Progress.from_dict(data)
    
    @staticmethod
    def get_student_progress(student_id, roadmap_id=None):
        """Get the latest progress for a student"""
        data_dir = 'data/storage'
        
        if not os.path.exists(data_dir):
            return None
            
        progress_entries = []
        
        for filename in os.listdir(data_dir):
            if filename.startswith('progress_') and filename.endswith('.json'):
                file_path = os.path.join(data_dir, filename)
                
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                if data.get('student_id') == student_id:
                    if roadmap_id is None or data.get('roadmap_id') == roadmap_id:
                        progress_entries.append(Progress.from_dict(data))
        
        if not progress_entries:
            return None
            
        # Return the most recent progress
        return sorted(progress_entries, key=lambda p: p.updated_at, reverse=True)[0]
    
    @staticmethod
    def save_feedback(feedback):
        """Save feedback data"""
        DataStore._ensure_data_dir()
        
        if not isinstance(feedback, Feedback):
            feedback = Feedback.from_dict(feedback)
            
        if not feedback.id:
            feedback.id = str(uuid.uuid4())
            
        file_path = f'data/storage/feedback_{feedback.id}.json'
        
        with open(file_path, 'w') as f:
            json.dump(feedback.to_dict(), f, indent=2)
            
        return feedback.id
    
    @staticmethod
    def get_feedback(feedback_id):
        """Get feedback data"""
        file_path = f'data/storage/feedback_{feedback_id}.json'
        
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        return Feedback.from_dict(data)
    
    @staticmethod
    def get_roadmap_feedback(roadmap_id):
        """Get all feedback for a roadmap"""
        data_dir = 'data/storage'
        
        if not os.path.exists(data_dir):
            return []
            
        feedback_entries = []
        
        for filename in os.listdir(data_dir):
            if filename.startswith('feedback_') and filename.endswith('.json'):
                file_path = os.path.join(data_dir, filename)
                
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                if data.get('roadmap_id') == roadmap_id:
                    feedback_entries.append(Feedback.from_dict(data))
        
        # Return feedback sorted by creation time
        return sorted(feedback_entries, key=lambda f: f.created_at)

# Add the missing functions here that are imported in app.py

def initialize_session_state():
    """Initialize the session state variables needed for the application"""
    # Initialize user if not already done
    SessionState.get_current_user()
    
    # Initialize other common session state variables
    if 'student_data' not in st.session_state:
        st.session_state.student_data = {}
    
    if 'roadmap' not in st.session_state:
        st.session_state.roadmap = None
    
    if 'progress_data' not in st.session_state:
        st.session_state.progress_data = {}
    
    if 'progress_analysis' not in st.session_state:
        st.session_state.progress_analysis = None
    
    if 'teacher_feedback' not in st.session_state:
        st.session_state.teacher_feedback = None
    
    if 'parent_feedback' not in st.session_state:
        st.session_state.parent_feedback = None
    
    if 'feedback_response' not in st.session_state:
        st.session_state.feedback_response = None
    
    if 'parent_response' not in st.session_state:
        st.session_state.parent_response = None
    
    if 'reconciled_feedback' not in st.session_state:
        st.session_state.reconciled_feedback = None

def save_state(data, data_type='student'):
    """Save the current state to persistent storage
    
    Args:
        data: The data to save
        data_type: Type of data ('student', 'roadmap', 'progress', 'feedback')
        
    Returns:
        str: ID of the saved data
    """
    if data_type == 'student':
        return DataStore.save_student(data)
    elif data_type == 'roadmap':
        return DataStore.save_roadmap(data)
    elif data_type == 'progress':
        return DataStore.save_progress(data)
    elif data_type == 'feedback':
        return DataStore.save_feedback(data)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

def load_state(id, data_type='student'):
    """Load state data from persistent storage
    
    Args:
        id: The ID of the data to load
        data_type: Type of data ('student', 'roadmap', 'progress', 'feedback')
        
    Returns:
        Object: The loaded data or None if not found
    """
    if data_type == 'student':
        return DataStore.get_student(id)
    elif data_type == 'roadmap':
        return DataStore.get_roadmap(id)
    elif data_type == 'progress':
        return DataStore.get_progress(id)
    elif data_type == 'feedback':
        return DataStore.get_feedback(id)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")