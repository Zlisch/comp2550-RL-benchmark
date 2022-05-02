---
title: "Get Conda Set Up to Run the Programs"
---

<!-- -->

# 1: Install Anaconda
Go to: https://docs.anaconda.com/anaconda/install/windows/ <br>
or the page relevant to your OS <br>
Follow the instructions to install Anaconda <br>
You should know that it is installed correctly when you type <code> conda -h </code> in your command prompt and help is displayed <br>

# 2: Create new conda environment:
Open a terminal in your coding environment (I am using VSCode) and create a new conda environment (can use different name): <br>
<code> conda create --name RLIPBM-py_10 python=3.10 </code> <br>

# 3: Activate environment:
<code> conda activate RLIPBM-py_10 </code> <br>
Note: python BMTemplateTester.py would currently throw an error because the packages are not installed <br>

# 4: Add necessary packages:
While in the conda environment: <br>
<code> conda install -c conda-forge pybox2d </code> <br>
<i> That install is (I think) why conda is necessary </i> <br>
<code> pip install pygame </code> <br>

# 5: Run the BMTemplateTester:
While in the conda environment: <br>
python BMTemplateTester.py <br>

# 6: Select the interpreter from this environment:
In VSCode, you can choose your interpreter to be this conda environment by having the Python Extension installed and by opening the command pallette and selecting 'select interpreter'. <br>
You can also use the command palette to create a new python terminal, which automaticlaly activates the selected conda environment!