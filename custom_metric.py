from typing import Any, Dict, Optional
from opik.evaluation.metrics import base_metric, score_result

class PsychologyMetric(base_metric.BaseMetric):
    """
    Custom metric for evaluating LLM responses in psychology research.
    This metric will be customized based on specific psychology research criteria.
    """
    
    def __init__(self, name: str = "psychology_evaluation"):
        """
        Initialize the psychology evaluation metric.
        
        Args:
            name: The name of the metric
        """
        self.name = name
    
    def score(self, context: str, output: str) -> score_result.ScoreResult:
        """
        Score the LLM output based on psychology research criteria.
        
        Args:
            context: The input/prompt given to the LLM
            output: The LLM's response
            
        Returns:
            A ScoreResult object containing the score and explanation
        """
        # This is a placeholder implementation
        # The actual implementation will be based on the prompt provided by the user
        
        # For demonstration purposes, we'll return a placeholder score
        return score_result.ScoreResult(
            value=0.5,  # Example score between 0 and 1
            name=self.name,
            reason="Placeholder evaluation for psychology research"
        )
    
    # Optionally, you can implement the ascore method for asynchronous scoring
    async def ascore(self, context: str, output: str) -> score_result.ScoreResult:
        """
        Asynchronous version of the score method.
        
        Args:
            context: The input/prompt given to the LLM
            output: The LLM's response
            
        Returns:
            A ScoreResult object containing the score and explanation
        """
        return await self.score(context, output)


# Alternative implementation using G-Eval
def create_psychology_geval_metric(task_introduction: Optional[str] = None, 
                                  evaluation_criteria: Optional[str] = None):
    """
    Create a psychology evaluation metric using G-Eval.
    
    Args:
        task_introduction: Custom task introduction for the G-Eval metric
        evaluation_criteria: Custom evaluation criteria for the G-Eval metric
        
    Returns:
        A G-Eval metric configured for psychology evaluation
    """
    from opik.evaluation.metrics import GEval
    
    # Default task introduction if none provided
    if task_introduction is None:
        task_introduction = """
        You are an expert in psychology research tasked with evaluating the quality 
        and relevance of an AI assistant's response to a psychology-related query.
        """
    
    # Default evaluation criteria if none provided
    if evaluation_criteria is None:
        evaluation_criteria = """
        Evaluate the response based on the following criteria:
        1. Scientific accuracy: Does the response align with established psychological theories and research?
        2. Clarity: Is the response clear and understandable?
        3. Relevance: Does the response directly address the query?
        4. Ethical considerations: Does the response consider ethical implications appropriately?
        
        Return only a score between 0 and 1:
        - 1.0: Excellent response that meets all criteria
        - 0.75: Good response with minor issues
        - 0.5: Adequate response with some significant issues
        - 0.25: Poor response with major issues
        - 0.0: Unacceptable response with critical issues
        
        The format of your response should be a JSON object with no additional text:
        {
          "score": <score between 0 and 1>
        }
        """
    
    # Create and return the G-Eval metric
    return GEval(
        task_introduction=task_introduction,
        evaluation_criteria=evaluation_criteria
    )
