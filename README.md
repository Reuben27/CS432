# CS 432
This repository contains the source code for all Assignment 3 of the Databases (CS 432) course by Prof. Mayank Singh.
The goal is to develop a DBMS using Flask and MySQl

## Getting Started

To set up the environment to run the assignment codes follow the below steps:

- You must have [Python](https://www.python.org/) and pip installed on your laptop/desktop. Run the following commands to check the whether you have them installed or not.
```
python --version
pip --version
```

- You must also have [git](https://git-scm.com/) installed on your laptop/desktop. Run the following command to check the same.
```
git --version
``` 

- Clone this git repository. Run git branch to ensure you are on the main branch. 
```
git clone https://github.com/Reuben27/CS432.git
git branch
```

- You must also have MySQL Workbench installed on your laptop/desktop. Run the following command in MySQL Command Client to create the database being used in the website. Here the path, is the path to the setup.sql file. For example, source E:\IITGn Academics\Semester VIII\CS 432 - Databases\Assignment 3\setup.sql
```
source <path>
```

- Install the packages from requirements.txt
```
pip install -r requirements.txt
```

- Run the app.py file 
```
python app.py
```