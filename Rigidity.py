from typing import List

# n: number of explained instances 
# S: n-sized list of 0s and 1s. [1,1,0, ... ,1,0,1] 
#    0s refer not supported decisions
#    1s refer supported decisions
# Calculate the support score based on the number of explained instances and the list of supported decisions.
def calculate_support(n: int, S: List[int]) -> float:
    return sum(S)/n
    
# S: n-sized list of 0s and 1s. [1,1,0, ... ,1,0,1] 
#    0s refer not supported decisions
#    1s refer supported decisions
# acc: accuracy score for between 0 and 1
# Calculate the rigidity based on the list of supported decisions and the accuracy score of the model.
def calculate_rigidity(S: List[int], acc: float) -> float:
    n = len(S)
    support = calculate_support(n, S)
    return abs(1 - support / acc)
