from agents.base_agent import BaseAgent

class MonitorAgent(BaseAgent):
    """Agent responsible for monitoring student progress"""
    
    def __init__(self, model_name=None):
        # Skip API initialization to avoid errors
        # super().__init__(model_name)
        pass
    
    def analyze_progress(self, roadmap, completed_tasks, time_spent, assessment_results):
        """Analyze student progress based on their updates"""
        # Simple progress analysis that doesn't rely on the API
        
        analysis = f"""# Progress Analysis

## Completed Tasks
{completed_tasks if completed_tasks else "No tasks reported as completed."}

## Time Spent
{time_spent if time_spent else "No time tracking reported."}

## Assessment Results
{assessment_results if assessment_results else "No assessment results reported."}

## Recommendations
1. **Continue With Your Plan**: Stay consistent with your study schedule
2. **Focus Areas**: Pay special attention to any topics where you scored below 80%
3. **Next Steps**: 
   - Review any concepts you found challenging
   - Increase practice for areas with lower assessment scores
   - Consider getting help with difficult topics

Continue tracking your progress and make adjustments to your study plan as needed.
"""
        return analysis