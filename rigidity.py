# n: number of explained instances 
# S: n-sized list of 0s and 1s. [1,1,0, ... ,1,0,1] 
#    0s refer not supported decisions
#    1s refer supported decisions
def support(n, S):
    return sum(S)/n
    
# S: n-sized list of 0s and 1s. [1,1,0, ... ,1,0,1] 
#    0s refer not supported decisions
#    1s refer supported decisions
# acc: accuracy score for between 0 and 1
def rigidity(S, acc):
    n = len(S)
    supp = support(n,S)
    return abs(1-supp/acc)
    