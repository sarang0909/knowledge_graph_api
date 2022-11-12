# knowledge_graph_api : Production Ready Code
 

https://user-images.githubusercontent.com/31824267/201452079-f5cf37b2-67f1-4dbe-85a4-4d8441932fa0.mp4



## About  
This is a project developed to create a code template for knowledge graph production ready api.    
Please note that information extraction model training is not done in this project.We've just used <a href="https://github.com/Babelscape/rebel">rebel</a> library and processed it's output.   


The basic code template for this project is derived from my another repo <a href="https://github.com/sarang0909/Code_Template">code template</a> 


### Requirement

Create knowledge graph api which accepts text data and gives information extraction triplets in the form of subject,object,relation.     
   
### Implementation   
Steps in creation of Knowledge Graph:   
Coreference Resolution    
Named Entity Recognition    
Entity Linking    
Relationship Extraction    
Knowledge Graph Creation    


1.Coreference Resolution:    
Convert pronouns to their original nouns.Refer my <a href="https://github.com/sarang0909/coreference_resolution_api">Coreference Resolution</a> project       
2.Named Entity Recognition(NER)      
We can skip this step and just get all relationships extracted. However, sometimes you 'll need only certain entities types and their relationships. We can extract default entities like NAME,PERSON etc from many available libraries or we can also build our own NER model. I've created a project to build custom NER-PERSON,ORG,PLACE,ROLE. But for knowledge graph,I am getting all relationships.
Refer my <a href="https://github.com/sarang0909/custom_ner_api">Custom NER</a> project.                
3.Entity Linking/Entity Disambiguation      
We can get different words/nouns for same entity. Example, U.S,United States of America,America. All these should be considered as one entity. We can achieve this by getting their root id if we have some knowledge base. Here, we are going to use Wikipedia knowledge. So, many time entity linking is also called as wikification.          
4.Relationship Extraction     
It means fetching relationships in text.     
I've explored couple of libraries- <a href="https://pypi.org/project/stanford-openie/1.0.1/"> Stanford Open IE</a> and <a href="https://github.com/Babelscape/rebel">rebel</a> libraries. 
I selected rebel for my final implementation because Stanford Open IE output was little redundant and it is slow.      
5.Knowledge Graph Creation     
I've explored neo4j python wrapper <a href="https://py2neo.org/2021.1/">py2neo</a> and <a href="https://networkx.org/">networkx</a> in a <a href="https://github.com/sarang0909/knowledge_graph_api/blob/master/src/training/graph_visualization.ipynb">notebook</a> and selected networkx just because ease of use for visualization. We should go for more powerful neo4j if want to use graph databases and perform further analysis but we are not doing that here.      



### Inference   
There are 2 ways to deploy this application.   
1. API using FastAPI.
2. Streamlit application

### Testing     
Unit test cases are written   

### Deployment 
Deployment is done locally using docker.   


## Code Oraganization   
Like any production code,this code is organized in following way:   
1. Keep all Requirement gathering documents in docs folder.       
2. Write and keep inference code in src/inference.   
3. Write Logging and configuration code in src/utility.      
4. Write unit test cases in tests folder.<a href="https://docs.pytest.org/en/7.1.x/">pytest</a>,<a href="https://pytest-cov.readthedocs.io/en/latest/readme.html">pytest-cov</a>    
5. Write performance test cases in tests folder.<a href="https://locust.io/">locust</a>     
6. Build docker image.<a href="https://www.docker.com/">Docker</a>  
7. Use and configure code formatter.<a href="https://black.readthedocs.io/en/stable/">black</a>     
8. Use and configure code linter.<a href="https://pylint.pycqa.org/en/latest/">pylint</a>     
9. Use Circle Ci for CI/CD.<a href="https://circleci.com/developer">Circlci</a>    
 
Clone this repo locally and add/update/delete as per your requirement.   
 
## Project Organization


├── README.md         		<- top-level README for developers using this project.    
├── pyproject.toml         		<- black code formatting configurations.    
├── .dockerignore         		<- Files to be ognored in docker image creation.    
├── .gitignore         		<- Files to be ignored in git check in.    
├── .circleci/config.yml         		<- Circleci configurations       
├── .pylintrc         		<- Pylint code linting configurations.    
├── Dockerfile         		<- A file to create docker image.    
├── environment.yml 	    <- stores all the dependencies of this project    
├── main.py 	    <- A main file to run API server.    
├── main_streamlit.py 	    <- A main file to run API server.  
├── src                     <- Source code files to be used by project.    
│       ├── inference 	        <- model output generator code   
│       ├── training 	        <- model training code  
│       ├── utility	        <- contains utility  and constant modules.   
├── logs                    <- log file path   
├── config                  <- config file path   
├── docs               <- documents from requirement,team collabaroation etc.   
├── tests               <- unit and performancetest cases files.   
│       ├── cov_html 	        <- Unit test cases coverage report    

## Installation
Development Environment used to create this project:  
Operating System: Windows 10 Home  

### Softwares
Anaconda:4.8.5  <a href="https://docs.anaconda.com/anaconda/install/windows/">Anaconda installation</a>   
 

### Python libraries:
Go to location of environment.yml file and run:  
```
conda env create -f environment.yml
```

 

## Usage
Here we have created ML inference on FastAPI server with dummy model output.

1. Go inside 'knowledge_graph_api' folder on command line.  
   Run:
  ``` 
      conda activate knowledge_graph_api  
      python main.py       
  ```
  Open 'http://localhost:5000/docs' in a browser.
![alt text](docs/fastapi_first.jpg?raw=true)
![alt text](docs/fastapi_second.jpg?raw=true)
 
2. Or to start Streamlit application  
5. Run:
  ``` 
      conda activate knowledge_graph_api  
      streamlit run main_streamlit.py 
  ```  






 
### Unit Testing
1. Go inside 'tests' folder on command line.
2. Run:
  ``` 
      pytest -vv 
      pytest --cov-report html:tests/cov_html --cov=src tests/ 
  ```
 
### Performance Testing
1. Open 2 terminals and start main application in one terminal  
  ``` 
      python main.py 
  ```

2. In second terminal,Go inside 'tests' folder on command line.
3. Run:
  ``` 
      locust -f locust_test.py  
  ```

### Black- Code formatter
1. Go inside 'knowledge_graph_api' folder on command line.
2. Run:
  ``` 
      black src 
  ```

### Pylint -  Code Linting
1. Go inside 'knowledge_graph_api' folder on command line.
2. Run:
  ``` 
      pylint src  
  ```

### Containerization
1. Go inside 'knowledge_graph_api' folder on command line.
2. Run:
  ``` 
      docker build -t myimage .  
      docker run -d --name mycontainer -p 5000:5000 myimage         
  ```


### CI/CD using Circleci
1. Add project on circleci website then monitor build on every commit.


### Note   
1.Spacy model not included,you can train your custom NER using my another <a href="https://github.com/sarang0909/custom_ner_api">Custom NER</a>project.    

## Contributing
Please create a Pull request for any change. 

## License


NOTE: This software depends on other packages that are licensed under different open source licenses.

