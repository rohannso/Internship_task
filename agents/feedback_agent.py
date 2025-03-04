from agents.base_agent import BaseAgent

class FeedbackAgent(BaseAgent):
    """Agent responsible for processing human feedback and generating responses"""
    
    def __init__(self, model_name=None):
        super().__init__(model_name)
        self.system_instructions = """
        You are an expert educational feedback coordinator. Your role is to:
        1. Process feedback from teachers and parents
        2. Identify key actionable insights from the feedback
        3. Generate appropriate responses and recommendations
        4. Prioritize feedback based on impact and urgency
        
        Be constructive, balanced, and focused on student success.
        """
    
    def process_teacher_feedback(self, roadmap, teacher_feedback):
        """Process teacher feedback and generate recommendations"""
    
    # First, format the template with the actual values
        formatted_prompt = f"""
    Please analyze the following teacher feedback on a student's roadmap:
    
    Roadmap:
    {roadmap}
    
    Teacher Feedback:
    {teacher_feedback}
    
    Based on this feedback, please provide:
    1. A summary of key points from the teacher
    2. Specific roadmap elements that need adjustment
    3. Prioritized recommendations for implementation
    4. A response to the teacher acknowledging their input
    
    Format your analysis in a clear, structured manner with actionable next steps.
    """
    
    # Then pass the formatted prompt to your chat functio
        prompt = self.create_chat_prompt(
        self.system_instructions,
        formatted_prompt
    )
    
        response = self.run_with_memory(prompt, {
        "roadmap": roadmap,
        "teacher_feedback": teacher_feedback
    })
        return response.content
    
    def process_parent_feedback(self, roadmap, parent_feedback):
        """Process parent feedback and generate recommendations"""
        prompt_template = """
        Please analyze the following parent feedback on a student's roadmap:
        
        Roadmap:
        {roadmap}
        
        Parent Feedback:
        {parent_feedback}
        
        Based on this feedback, please provide:
        1. A summary of key points from the parent
        2. Contextual factors that might impact the roadmap
        3. Balanced recommendations that consider both academic goals and home context
        4. A response to the parent acknowledging their input
        
        Format your analysis in a clear, structured manner with actionable next steps.
        """
        
        prompt = self.create_chat_prompt(
            self.system_instructions,
            prompt_template
        )
        
        response = self.run_with_memory(prompt, {
            "roadmap": roadmap,
            "parent_feedback": parent_feedback
        })
        
        return response.content
    
    def reconcile_feedback(self, teacher_feedback, parent_feedback, student_input):
        """Reconcile potentially conflicting feedback from different sources"""
        prompt_template = """
        Please reconcile the following feedback from different stakeholders:
        
        Teacher Feedback:
        {teacher_feedback}
        
        Parent Feedback:
        {parent_feedback}
        
        Student Input:
        {student_input}
        
        Please provide:
        1. Areas of agreement between stakeholders
        2. Points of conflict or tension
        3. Balanced recommendations that address key concerns
        4. A prioritized list of actionable adjustments
        
        Format your recommendations in a diplomatic, balanced manner that respects all perspectives.
        """
        
        prompt = self.create_chat_prompt(
            self.system_instructions,
            prompt_template
        )
        
        response = self.run_with_memory(prompt, {
            "teacher_feedback": teacher_feedback,
            "parent_feedback": parent_feedback,
            "student_input": student_input
        })
        
        return response.content