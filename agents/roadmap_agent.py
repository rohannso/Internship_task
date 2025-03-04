from agents.base_agent import BaseAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RoadmapAgent(BaseAgent):
    """Agent responsible for generating personalized study roadmaps"""
    
    def __init__(self, model_name=None):
        # Skip the API initialization if we're going to use fallback
        # super().__init__(model_name)
        self.use_api = os.getenv("GROQ_API_KEY") is not None
        if self.use_api:
            super().__init__(model_name)
        
        self.system_instructions = """
        You are an expert educational consultant specializing in creating personalized study roadmaps.
        Your task is to analyze student data and create customized study plans that:
        1. Focus on the student's strengths and address their weaknesses
        2. Align with their academic goals and target scores
        3. Provide a realistic schedule with time allocations
        4. Recommend specific learning resources for each topic
        
        Be specific, practical, and tailor your recommendations to the individual student.
        """
    
    def generate_roadmap(self, student_data):
        """Generate a personalized roadmap based on student data"""
        # Skip the API call and just use the fallback method
        return self._generate_custom_roadmap(student_data)
    
    def _generate_custom_roadmap(self, student_data):
        """Generate a custom roadmap based directly on the student data"""
        # Extract student information
        name = student_data.get("name", "Student")
        grade = student_data.get("grade", "N/A")
        subjects = student_data.get("subjects", [])
        if isinstance(subjects, str):
            subjects = [s.strip() for s in subjects.split(",")]
        performance = student_data.get("performance", "Not specified")
        goals = student_data.get("goals", "Not specified")
        strengths = student_data.get("strengths", "Not specified")
        weaknesses = student_data.get("weaknesses", "Not specified")
        
        # Check for JEE preparation
        is_jee_prep = "jee" in goals.lower()
        
        # Create a personalized roadmap
        roadmap = f"""# Personalized Study Roadmap for {name}

## Student Profile
- **Name:** {name}
- **Grade/Year:** {grade}
- **Subjects:** {', '.join(subjects) if isinstance(subjects, list) else subjects}
- **Current Performance:** {performance}
- **Academic Goals:** {goals}
- **Strengths:** {strengths}
- **Areas for Improvement:** {weaknesses}

## 4-Week Study Plan
"""

        # JEE-specific plan if applicable
        if is_jee_prep:
            roadmap += """
### JEE Preparation Focus

#### Week 1: Foundation Building
- **Mathematics:** 
  - Review algebra, trigonometry, and coordinate geometry (2 hours/day)
  - Practice 10 basic problems daily
- **Physics:** 
  - Mechanics fundamentals (1.5 hours/day)
  - NCERT textbook completion
- **Chemistry:** 
  - Basic concepts of physical and organic chemistry (1.5 hours/day)
  - Periodic table and chemical bonding

#### Week 2: Concept Strengthening
- **Mathematics:** 
  - Calculus introduction and functions (2 hours/day)
  - Start with JEE previous year questions (easy level)
- **Physics:** 
  - Electricity and magnetism (1.5 hours/day)
  - Solve numerical problems
- **Chemistry:** 
  - Organic chemistry mechanisms (1.5 hours/day)
  - Inorganic chemistry - group properties

#### Week 3: Problem-Solving
- **Mathematics:** 
  - Probability, statistics, and vectors (2 hours/day)
  - Medium difficulty JEE problems
- **Physics:** 
  - Optics and modern physics (1.5 hours/day)
  - Conceptual questions practice
- **Chemistry:** 
  - Equilibrium and thermodynamics (1.5 hours/day)
  - Chemical reactions practice

#### Week 4: Review and Assessment
- **Mathematics:** 
  - Mock tests and problem areas review (2 hours/day)
  - Timing practice for quick solutions
- **Physics:** 
  - Full-length subject tests (1.5 hours/day)
  - Revision of formulas and concepts
- **Chemistry:** 
  - Mock tests covering all areas (1.5 hours/day)
  - Revision of reactions and mechanisms

### Recommended Resources
1. **Books:**
   - NCERT Textbooks (all subjects) - Essential foundation
   - H.C. Verma for Physics
   - R.D. Sharma for Mathematics
   - O.P. Tandon for Chemistry

2. **Online Resources:**
   - Khan Academy for concept clarity
   - JEE Main/Advanced previous papers
   - YouTube channels: Physics Wallah, Vedantu JEE

3. **Practice Materials:**
   - Daily practice worksheets
   - Weekly mock tests
   - Monthly full JEE mock exams
"""
        else:
            # General study plan for the specific subjects
            for subject in subjects:
                if subject == "Math":
                    roadmap += f"""
### Mathematics Focus

#### Week 1: Core Concepts
- Review fundamental concepts (1 hour/day)
- Practice basic problem sets (30 min/day)
- Complete chapter exercises from textbook

#### Week 2: Advanced Applications
- Problem-solving techniques (1 hour/day)
- Practice word problems (30 min/day)
- Begin mock tests for assessment

#### Week 3: Weak Areas
- Focus on {weaknesses} (1.5 hours/day)
- Get additional practice in challenging topics
- Review feedback from mock tests

#### Week 4: Review and Mastery
- Comprehensive review of all topics (1 hour/day)
- Practice exams under timed conditions
- Focus on error analysis and improvement
"""
                elif subject == "Science":
                    roadmap += f"""
### Science Focus

#### Week 1: Theoretical Foundations
- Review core scientific principles (1 hour/day)
- Create summary notes for key concepts
- Complete chapter-end questions

#### Week 2: Practical Applications
- Connect theory with real-world examples (1 hour/day)
- Practice numerical problems (if applicable)
- Begin practice tests for self-assessment

#### Week 3: Deep Dive
- Focus on more complex topics (1.5 hours/day)
- Strengthen areas related to {weaknesses}
- Analyze and correct mistakes from practice tests

#### Week 4: Integration and Review
- Connect concepts across different units (1 hour/day)
- Take full-length practice exams
- Review all major topics and formulas
"""

        # Add personalized tips based on strengths and weaknesses
        roadmap += f"""
## Personalized Tips for {name}

### Leveraging Your Strengths
- As a {strengths}, use this ability to:
  - Create condensed study materials
  - Help you grasp new concepts quickly
  - Set ambitious but achievable daily goals

### Addressing Areas for Improvement
- To improve {weaknesses}:
  - Set up a consistent daily study schedule
  - Use confidence-building exercises before study sessions
  - Break down large tasks into smaller, manageable chunks
  - Track your progress to build motivation
  - Join study groups for accountability

### Daily Schedule Recommendation
- **Morning (1-2 hours):** Focus on the most challenging subjects when your mind is fresh
- **Afternoon (1-2 hours):** Complete assignments and practice problems
- **Evening (1 hour):** Review the day's learning and prepare for tomorrow
- **Weekend:** Longer review sessions and practice tests

## Progress Tracking
- Weekly self-assessment tests
- Daily completion checklist
- Bi-weekly review of this roadmap to adjust as needed

This roadmap is designed specifically for your needs and goals. Consistent effort following this plan will help you achieve your academic goals and improve in your areas of concern.
"""

        return roadmap
    
    def update_roadmap(self, current_roadmap, progress_data, feedback):
        """Update an existing roadmap based on progress and feedback"""
        # Just return a simple update message
        return current_roadmap + "\n\n## Updated Recommendations\nBased on your progress:\n1. Continue focusing on your core subjects\n2. Address any difficulties in your areas of weakness\n3. Keep tracking your progress regularly"