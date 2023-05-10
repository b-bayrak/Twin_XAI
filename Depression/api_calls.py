from mycbr_py_api import MyCBRRestApi as mycbr
import requests
from requests import get
import pandas as pd


# Variables that are related to current CBR project
concept = 'case' 

# API connection

server = 'localhost'
#server = 'user@hv-6066.idi.ntnu.no'

port = '8080'
base_url = 'http://' + server + ':' + port + '/'

headers = {'Content-type':'application/json'}

obj = mycbr(base_url)

# Compare answers with query values
def rowExpFlip(row, exp):
    lst = []
    for i in range(len(row)):
        if bool(row.iloc[i]) == exp.iloc[i]['Value']:
            lst.append(1)
        else:
            lst.append(0)
    return lst


# Calculate 'Matched' value for a query
def calculateMatched(row):
    # Exploring expected answers (domain knowledge)
    expected_answers = pd.read_csv('./expectedanswers.txt', sep = '\\*\\*')
    expected_answers.columns = ['Question', 'Value']

    expected_answers.head()
    expected_answers = expected_answers.T
    expected_answers.columns = ['t' + str(col) for col in expected_answers.columns]    
    comp_list = rowExpFlip(row, expected_answers.T)

  
    return sum(comp_list)

# Deletes all cases from specified concept 
def delete_instances_from_concept(c):
    response = requests.delete('http://localhost:8080/concepts/'+c+'/cases')
    print("cases deleted from " + c + ": " + str(response.ok))
    
# Adds a new casebase 
def put_new_cb(newCbName):
    requests.put(base_url + 'casebases/' + newCbName)
    
# Returns casebase list
def get_casebases():
    raw = pd.DataFrame(requests.get(base_url + 'casebases/').json())
    casebases = pd.DataFrame.from_records(raw).values.tolist()
    return casebases

# add cases to casebase
def add_rows_as_cases(x, c, cb):
    case_id = 'case_' + str(x['index'])
    x = x.drop(['Target', 'index'])
    requests.put(base_url + 'concepts/' + c + '/casebases/' + cb +'/cases/' + case_id, data = str(x.to_json()), headers=headers)

# add cases to casebase from dataframe
def add_cases_from_df(df, c, cb):  
    tmp = df.copy(deep=True)
    tmp.reset_index(inplace=True)
    tmp.apply(add_rows_as_cases, args=(c, cb), axis=1)
    
# Rename indices of shap values (like 't0, t1')    
def rename_indices(idx):
    indx = []
    for i in range(len(idx)-1,-1,-1):
        indx.append('t'+str(idx[i]))
    return indx

# Add new amalgamation function
def newAmalgamationFunc(c, amalFuncID, amalFuncType, json):
    return requests.put(base_url + 'concepts/' + c + '/amalgamationFunctions?amalgamationFunctionID=' + amalFuncID + '&amalgamationFunctionType=' + amalFuncType + '&attributeWeightsJSON=' + json)

# Retrieves similar cases from given casebase
def query_cbr_system(concept, casebase, amalgamationFct, queryJSON, k=-1):
    #print(obj.getAllCasesFromCaseBase(concept, casebase).shape)
    raw = requests.post(base_url + 'concepts/' + concept + '/casebases/' + casebase + '/amalgamationFunctions/' + amalgamationFct +'/retrievalByMultipleAttributes?k='+ str(k), 
                        data=str(queryJSON),
                        headers = headers)
    results = pd.DataFrame.from_dict(raw.json())
    results = results.apply(pd.to_numeric, errors='coerce').fillna(results).sort_values(by='similarity', ascending=False)
    return results[['caseID', 'similarity']]


# Returns a dataframe of similar cases from all casebases
def query_all_cbr_systems(concept, query, k):
    class_0_cbr_results = query_cbr_system(concept, 'cb_class0', 'amal_func_class0', query.to_json(), k)
    if 1 in class_0_cbr_results.similarity.values:
        class_0_cbr_results = query_cbr_system(concept, 'cb_class0', 'amal_func_class0', query.to_json(), k+1)    
        class_0_cbr_results = class_0_cbr_results[1:].reset_index(drop=True)
    class_0_cbr_results.columns = ['caseID_c0', 'similarity_c0']
    
    class_1_cbr_results = query_cbr_system(concept, 'cb_class1', 'amal_func_class1', query.to_json(), k)
    if 1 in class_1_cbr_results.similarity.values:
        class_1_cbr_results = query_cbr_system(concept, 'cb_class1', 'amal_func_class1', query.to_json(), k+1)    
        class_1_cbr_results = class_1_cbr_results[1:].reset_index(drop=True)
    class_1_cbr_results.columns = ['caseID_c1', 'similarity_c1']
    
    class_2_cbr_results = query_cbr_system(concept, 'cb_class2', 'amal_func_class2', query.to_json(), k)
    if 1 in class_2_cbr_results.similarity.values:
        class_2_cbr_results = query_cbr_system(concept, 'cb_class2', 'amal_func_class2', query.to_json(), k+1)    
        class_2_cbr_results = class_2_cbr_results[1:].reset_index(drop=True)
    class_2_cbr_results.columns = ['caseID_c2', 'similarity_c2']
    
    return pd.concat([class_0_cbr_results, class_1_cbr_results, class_2_cbr_results], axis=1)

# Returns class information of most similar case 
def get_class_from_cbr_results(x):
    classid = 5
    class_list = [x.similarity_c0, x.similarity_c1, x.similarity_c2]
    classid =class_list.index(max(class_list))
    return classid