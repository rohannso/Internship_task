from typing import List, Dict, Optional, Any
from datetime import datetime

class Student:
    """Student data model"""
    
    def __init__(
        self,
        id: str,
        name: str,
        grade: str,
        subjects: List[str],
        strengths: List[str] = None,
        weaknesses: List[str] = None,
        goals: Dict[str, Any] = None,
        performance: Dict[str, Any] = None
    ):
        self.id = id
        self.name = name
        self.grade = grade
        self.subjects = subjects
        self.strengths = strengths or []
        self.weaknesses = weaknesses or []
        self.goals = goals or {}
        self.performance = performance or {}
        
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade,
            "subjects": self.subjects,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "goals": self.goals,
            "performance": self.performance
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            grade=data.get("grade"),
            subjects=data.get("subjects", []),
            strengths=data.get("strengths", []),
            weaknesses=data.get("weaknesses", []),
            goals=data.get("goals", {}),
            performance=data.get("performance", {})
        )


class Roadmap:
    """Roadmap data model"""
    
    def __init__(
        self,
        id: str,
        student_id: str,
        content: str,
        created_at: datetime = None,
        updated_at: datetime = None,
        version: int = 1,
        approved_by: str = None
    ):
        self.id = id
        self.student_id = student_id
        self.content = content
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.version = version
        self.approved_by = approved_by
        
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version,
            "approved_by": self.approved_by
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        return cls(
            id=data.get("id"),
            student_id=data.get("student_id"),
            content=data.get("content"),
            created_at=datetime.fromisoformat(data.get("created_at")) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data.get("updated_at")) if data.get("updated_at") else None,
            version=data.get("version", 1),
            approved_by=data.get("approved_by")
        )


class Progress:
    """Student progress data model"""
    
    def __init__(
        self,
        id: str,
        student_id: str,
        roadmap_id: str,
        completed_tasks: Dict[str, bool] = None,
        time_spent: Dict[str, int] = None,
        assessment_results: List[Dict[str, Any]] = None,
        notes: str = None,
        updated_at: datetime = None
    ):
        self.id = id
        self.student_id = student_id
        self.roadmap_id = roadmap_id
        self.completed_tasks = completed_tasks or {}
        self.time_spent = time_spent or {}
        self.assessment_results = assessment_results or []
        self.notes = notes
        self.updated_at = updated_at or datetime.now()
        
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "roadmap_id": self.roadmap_id,
            "completed_tasks": self.completed_tasks,
            "time_spent": self.time_spent,
            "assessment_results": self.assessment_results,
            "notes": self.notes,
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        return cls(
            id=data.get("id"),
            student_id=data.get("student_id"),
            roadmap_id=data.get("roadmap_id"),
            completed_tasks=data.get("completed_tasks", {}),
            time_spent=data.get("time_spent", {}),
            assessment_results=data.get("assessment_results", []),
            notes=data.get("notes"),
            updated_at=datetime.fromisoformat(data.get("updated_at")) if data.get("updated_at") else None
        )


class Feedback:
    """Feedback data model"""
    
    def __init__(
        self,
        id: str,
        student_id: str,
        roadmap_id: str,
        source_type: str,  # "teacher", "parent", or "student"
        source_id: str,
        content: str,
        created_at: datetime = None,
        processed: bool = False,
        response: str = None
    ):
        self.id = id
        self.student_id = student_id
        self.roadmap_id = roadmap_id
        self.source_type = source_type
        self.source_id = source_id
        self.content = content
        self.created_at = created_at or datetime.now()
        self.processed = processed
        self.response = response
        
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "roadmap_id": self.roadmap_id,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "processed": self.processed,
            "response": self.response
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        return cls(
            id=data.get("id"),
            student_id=data.get("student_id"),
            roadmap_id=data.get("roadmap_id"),
            source_type=data.get("source_type"),
            source_id=data.get("source_id"),
            content=data.get("content"),
            created_at=datetime.fromisoformat(data.get("created_at")) if data.get("created_at") else None,
            processed=data.get("processed", False),
            response=data.get("response")
        )

# Add aliases for the classes that app.py is trying to import
StudentData = Student
ProgressData = Progress
FeedbackData = Feedback