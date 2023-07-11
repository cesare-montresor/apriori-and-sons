# apriori-and-sons
This repo contains several variants of the apriori and son algorithms

# Usage 

## Generate TaskList

```bash
python main.py tasklist
```
Generates a list of tasks in the form as executable tasks_.sh file, in the result/ folder.
For the time being, the list of task is generated from the configuration in the top part of main.py.
**IMPORTANT** Work in progress: is recomanded to copy the tasks_.sh file to the main folder before runing it.

## Run a task
```bash
python main.py runtask <task_name> <algo_name> <min_support> <data_path> <result_path> <index_path>
```
Run a task, given the spcified parameters, is used inside the tasks_.sh. 
Can be also used manually.
Results are generated inside the result/ folder, each having a dedicated folder, named like the task.
New results for the same task name, will override previous ones.

## Generates Dataset Statistics
```bash
python main.py datastats
```
Generate a CVS file containing Statistics and Charts. 
Charts data consist of last 4 CSV files.
The name of the field specify the axis (x,y) and the name of the chart.
Inside each field the dataserie is separeted by "|" char.




# Setup
- Install Spark
- Install conda
- Add Hadoop native libs


```bash
conda create --name <envname> --file requirements.txt
```


```bash
sudo systemctl enable ssh    
sudo apt install openssh-server
sudo apt install screen
```



# Datasets
- Frequent Itemset Mining Dataset Repository    
http://fimi.uantwerpen.be/data/
- Mirror
http://www.cs.rpi.edu/~zaki/Workshops/FIMI/data/     
- Generator
www.miles.cnuce.cnr.it/~palmeri/datam/DCI/
