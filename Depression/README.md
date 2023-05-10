## Setup
### Starting the API
We assume that you have cloned the GitHub repository and added the mycbr-rest-2.0.jar into the mycbr folder of this repository. Then in the terminal, navigate to the cloned project folder. 

Then go into the mycbr folder and run the following command:
```
java -DMYCBR.PROJECT.FILE=project/XCBR_Psychology_Prediction_3classes.prj -jar mycbr-rest-2.0.jar
```
This command will start a local webserver, deploy the myCBR project and expose it's endpoints via a Rest API. We assume that this server is running in the background while the experiments notebooks are run.

### Accesing API

Once the installation is done and the API is running, the API will be accessibleat http://localhost:8080/swagger-ui.html#. To verify that the API is up and running, please check that you can see the swagger documentation page for the API.

## Experiments

### Necessary files to run the Experiments

To run our experiments we provide 'WineQuality' and 'Depression' folders with a number of files. The folders consists of experiments and the following folders to reproduce the experiments:
- project/: contains project files that are modelled for the experiments. 
- data/: contains the train and test .csv files needed for the experiments. Those are created based on the given datasets. They are the results after we conducted the first set of experiments to find a good split of the provided data. 
- model/: contains the .pkl files for the BB models used in the experiments.
- shap/: contains the shap values per class .csv files needed to create the global similarity functions of the CBR agents.


###  Exp_1_compare_CBR_BB.ipynb
- Compare CBR Systems' performance with Black-box models.

### Exp_2_compare_CBR_domain.ipynb
- Compare CBR Systems' performance with and without domain knowledge ('Matched' attribute).

### Exp_3_MAS_explains_BB.ipynb
- Import cases to the project, set amalgamation functions for each casbase. Generate explanations for every instance in the test set and calculate rigidity of the explanation system.


