from datetime import datetime, timedelta
import random

def get_sample_student_data():
    """Generate sample student data for testing the application."""
    
    # Current date
    current_date = datetime.now()
    
    # Sample student data
    student_data = {
        "name": "Aditya Sharma",
        "grade": "Class 11",
        "target_exam": "JEE",
        "target_score": "95%",
        "current_progress": 78,  # percentage
        "subjects": [
            {
                "name": "Physics",
                "score": 82,
                "topics": [
                    {"name": "Mechanics", "score": 85, "mastery": "High"},
                    {"name": "Electromagnetism", "score": 72, "mastery": "Medium"},
                    {"name": "Optics", "score": 68, "mastery": "Low"},
                    {"name": "Modern Physics", "score": 75, "mastery": "Medium"}
                ]
            },
            {
                "name": "Chemistry",
                "score": 75,
                "topics": [
                    {"name": "Physical Chemistry", "score": 80, "mastery": "High"},
                    {"name": "Organic Chemistry", "score": 65, "mastery": "Low"},
                    {"name": "Inorganic Chemistry", "score": 78, "mastery": "Medium"}
                ]
            },
            {
                "name": "Mathematics",
                "score": 88,
                "topics": [
                    {"name": "Algebra", "score": 90, "mastery": "High"},
                    {"name": "Calculus", "score": 85, "mastery": "High"},
                    {"name": "Coordinate Geometry", "score": 82, "mastery": "Medium"},
                    {"name": "Trigonometry", "score": 76, "mastery": "Medium"}
                ]
            }
        ],
        
        # Daily tasks
        "daily_tasks": [
            {
                "id": 1,
                "title": "Solve 20 Physics problems",
                "subject": "Physics",
                "time_slot": "morning",
                "start_time": "9:00 AM",
                "end_time": "10:30 AM",
                "completed": False,
                "description": "Solve problems from the mechanics chapter focusing on projectile motion.",
                "resources": [
                    {"title": "HC Verma Chapter 5", "url": "https://example.com/hcverma-ch5"},
                    {"title": "Video Tutorial: Projectile Motion", "url": "https://example.com/projectile-motion"}
                ],
                "related_topics": ["Mechanics", "Projectile Motion", "Circular Motion"]
            },
            {
                "id": 2,
                "title": "Chemistry Revision",
                "subject": "Chemistry",
                "time_slot": "afternoon",
                "start_time": "2:00 PM",
                "end_time": "3:30 PM",
                "completed": True,
                "description": "Revise organic chemistry reactions from chapter 12.",
                "resources": [
                    {"title": "NCERT Chapter 12 Notes", "url": "https://example.com/ncert-chem-ch12"},
                    {"title": "Reaction Mechanisms PDF", "url": "https://example.com/reaction-mechanisms"}
                ],
                "related_topics": ["Organic Chemistry", "Reaction Mechanisms"]
            },
            {
                "id": 3,
                "title": "Math Practice Test",
                "subject": "Mathematics",
                "time_slot": "evening",
                "start_time": "6:00 PM",
                "end_time": "7:30 PM",
                "completed": False,
                "description": "Complete practice test on differential calculus.",
                "resources": [
                    {"title": "Practice Test PDF", "url": "https://example.com/calculus-test"},
                    {"title": "Formula Sheet", "url": "https://example.com/calculus-formulas"}
                ],
                "related_topics": ["Calculus", "Differentiation", "Applications"]
            }
        ],
        
        # Weekly data
        "current_week": 4,
        "weeks_data": [
            {
                "week": 1,
                "subject_hours": {
                    "Physics": 10,
                    "Chemistry": 8,
                    "Mathematics": 12
                },
                "schedule": {
                    "Monday": {
                        "Morning": [{"title": "Physics Lecture", "subject": "Physics"}],
                        "Afternoon": [{"title": "Chemistry Lab", "subject": "Chemistry"}],
                        "Evening": [{"title": "Math Problem Solving", "subject": "Mathematics"}]
                    },
                    "Tuesday": {
                        "Morning": [{"title": "Mathematics Revision", "subject": "Mathematics"}],
                        "Afternoon": [{"title": "Physics Problems", "subject": "Physics"}],
                        "Evening": [{"title": "Chemistry Notes", "subject": "Chemistry"}]
                    },
                    "Wednesday": {
                        "Morning": [{"title": "Chemistry Lecture", "subject": "Chemistry"}],
                        "Afternoon": [{"title": "Mathematics Class", "subject": "Mathematics"}],
                        "Evening": [{"title": "Physics Revision", "subject": "Physics"}]
                    },
                    "Thursday": {
                        "Morning": [{"title": "Physics Lecture", "subject": "Physics"}],
                        "Afternoon": [{"title": "Mathematics Problems", "subject": "Mathematics"}],
                        "Evening": [{"title": "Chemistry Practice", "subject": "Chemistry"}]
                    },
                    "Friday": {
                        "Morning": [{"title": "Mathematics Lecture", "subject": "Mathematics"}],
                        "Afternoon": [{"title": "Physics Lab", "subject": "Physics"}],
                        "Evening": [{"title": "Chemistry Revision", "subject": "Chemistry"}]
                    },
                    "Saturday": {
                        "Morning": [{"title": "Practice Test", "subject": "All Subjects"}],
                        "Afternoon": [{"title": "Doubt Clearing", "subject": "All Subjects"}],
                        "Evening": [{"title": "Self Study", "subject": "Weak Areas"}]
                    },
                    "Sunday": {
                        "Morning": [{"title": "Revision", "subject": "All Subjects"}],
                        "Afternoon": [{"title": "Rest", "subject": ""}],
                        "Evening": [{"title": "Plan Next Week", "subject": ""}]
                    }
                },
                "focus_areas": [
                    {"subject": "Physics", "topic": "Mechanics Basics"},
                    {"subject": "Chemistry", "topic": "Periodic Table"},
                    {"subject": "Mathematics", "topic": "Fundamental Algebra"}
                ],
                "assessments": [
                    {"title": "Physics Quiz", "day": "Wednesday", "description": "30-minute quiz on mechanics"},
                    {"title": "Math Test", "day": "Friday", "description": "1-hour test on algebra"}
                ]
            },
            # Week 2
            {
                "week": 2,
                "subject_hours": {
                    "Physics": 9,
                    "Chemistry": 10,
                    "Mathematics": 11
                },
                "schedule": {
                    "Monday": {
                        "Morning": [{"title": "Physics Lecture", "subject": "Physics"}],
                        "Afternoon": [{"title": "Chemistry Lab", "subject": "Chemistry"}],
                        "Evening": [{"title": "Math Problem Solving", "subject": "Mathematics"}]
                    },
                    "Tuesday": {
                        "Morning": [{"title": "Mathematics Revision", "subject": "Mathematics"}],
                        "Afternoon": [{"title": "Physics Problems", "subject": "Physics"}],
                        "Evening": [{"title": "Chemistry Notes", "subject": "Chemistry"}]
                    },
                    "Wednesday": {
                        "Morning": [{"title": "Chemistry Lecture", "subject": "Chemistry"}],
                        "Afternoon": [{"title": "Mathematics Class", "subject": "Mathematics"}],
                        "Evening": [{"title": "Physics Revision", "subject": "Physics"}]
                    },
                    "Thursday": {
                        "Morning": [{"title": "Physics Lecture", "subject": "Physics"}],
                        "Afternoon": [{"title": "Mathematics Problems", "subject": "Mathematics"}],
                        "Evening": [{"title": "Chemistry Practice", "subject": "Chemistry"}]
                    },
                    "Friday": {
                        "Morning": [{"title": "Mathematics Lecture", "subject": "Mathematics"}],
                        "Afternoon": [{"title": "Physics Lab", "subject": "Physics"}],
                        "Evening": [{"title": "Chemistry Revision", "subject": "Chemistry"}]
                    },
                    "Saturday": {
                        "Morning": [{"title": "Practice Test", "subject": "All Subjects"}],
                        "Afternoon": [{"title": "Doubt Clearing", "subject": "All Subjects"}],
                        "Evening": [{"title": "Self Study", "subject": "Weak Areas"}]
                    },
                    "Sunday": {
                        "Morning": [{"title": "Revision", "subject": "All Subjects"}],
                        "Afternoon": [{"title": "Rest", "subject": ""}],
                        "Evening": [{"title": "Plan Next Week", "subject": ""}]
                    }
                },
                "focus_areas": [
                    {"subject": "Physics", "topic": "Electricity Basics"},
                    {"subject": "Chemistry", "topic": "Organic Chemistry"},
                    {"subject": "Mathematics", "topic": "Calculus Fundamentals"}
                ],
                "assessments": [
                    {"title": "Chemistry Quiz", "day": "Wednesday", "description": "30-minute quiz on organic chemistry"},
                    {"title": "Physics Test", "day": "Friday", "description": "1-hour test on electricity"}
                ]
            },

            # Week 3
            {
                "week": 3,
                "subject_hours": {
                    "Physics": 11,
                    "Chemistry": 8,
                    "Mathematics": 9
                },
                "schedule": {
                    "Monday": {
                        "Morning": [{"title": "Physics Lecture", "subject": "Physics"}],
                        "Afternoon": [{"title": "Chemistry Lab", "subject": "Chemistry"}],
                        "Evening": [{"title": "Math Problem Solving", "subject": "Mathematics"}]
                    },
                    "Tuesday": {
                        "Morning": [{"title": "Mathematics Revision", "subject": "Mathematics"}],
                        "Afternoon": [{"title": "Physics Problems", "subject": "Physics"}],
                        "Evening": [{"title": "Chemistry Notes", "subject": "Chemistry"}]
                    },
                    "Wednesday": {
                        "Morning": [{"title": "Chemistry Lecture", "subject": "Chemistry"}],
                        "Afternoon": [{"title": "Mathematics Class", "subject": "Mathematics"}],
                        "Evening": [{"title": "Physics Revision", "subject": "Physics"}]
                    },
                    "Thursday": {
                        "Morning": [{"title": "Physics Lecture", "subject": "Physics"}],
                        "Afternoon": [{"title": "Mathematics Problems", "subject": "Mathematics"}],
                        "Evening": [{"title": "Chemistry Practice", "subject": "Chemistry"}]
                    },
                    "Friday": {
                        "Morning": [{"title": "Mathematics Lecture", "subject": "Mathematics"}],
                        "Afternoon": [{"title": "Physics Lab", "subject": "Physics"}],
                        "Evening": [{"title": "Chemistry Revision", "subject": "Chemistry"}]
                    },
                    "Saturday": {
                        "Morning": [{"title": "Practice Test", "subject": "All Subjects"}],
                        "Afternoon": [{"title": "Doubt Clearing", "subject": "All Subjects"}],
                        "Evening": [{"title": "Self Study", "subject": "Weak Areas"}]
                    },
                    "Sunday": {
                        "Morning": [{"title": "Revision", "subject": "All Subjects"}],
                        "Afternoon": [{"title": "Rest", "subject": ""}],
                        "Evening": [{"title": "Plan Next Week", "subject": ""}]
                    }       
                },  

                "focus_areas": [
                    {"subject": "Physics", "topic": "Optics Basics"},
                    {"subject": "Chemistry", "topic": "Chemical Reactions"},
                    {"subject": "Mathematics", "topic": "Probability Concepts"}
                ],
                "assessments": [
                    {"title": "Mathematics Quiz", "day": "Wednesday", "description": "30-minute quiz on probability"},
                    {"title": "Chemistry Test", "day": "Friday", "description": "1-hour test on chemical reactions"}
                ]

            },

            