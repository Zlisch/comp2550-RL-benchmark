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
[Update: it is OK to skip create new conda environment (step 2 & 3), so the box2d can be installed in the base environment. 
Have box2d in the base environment allows IDE to recognize box2d classes and allow IDE to directly run the application!]

Open a terminal in your coding environment (I am using VSCode) and create a new conda environment (can use different name): <br>
<code> conda create --name RLIPBM-py_10 python=3.10 </code> <br>

# 3: Activate environment:
[Update: it is OK to skip create new conda environment (step 2 & 3), so the box2d can be installed in the base environment. 
Have box2d in the base environment allows IDE to recognize box2d classes and allow IDE to directly run the application!]

<code> conda activate RLIPBM-py_10 </code> <br>
Note: python BMTemplateTester.py would currently throw an error because the packages are not installed <br>

# 4: Add necessary packages:
While in the conda environment: <br>
<code> conda install -c conda-forge pybox2d </code> <br>
<i> That install is (I think) why conda is necessary </i> <br>
<code> pip install pygame </code> <br>
<br>
We might also be needing Tensorflow soon: <br>
<code> pip install tensorflow </code> <br>
<code> pip install tf-agents </code> <br>

# 5: Run the BMTemplateTester:
While in the conda environment: <br>
python BMTemplateTester.py <br>

# 5B: Instead of run the BMTemplateTester, run BMApplication: 
Move to source code dictionary if currently in the root dictionary: 

<code> cd src </code> <br>

While in the source code dictionary, run the BMApplication by: 

<code> python BMApplication.py seesaw </code> <br>

The following parameters can be specified for the application: 
- t (template): required, indicate use which template, can be roof, seesaw...
- v (variant number): optional, generate variant task from the template, range=[0.0,1.0], default=0.0
- a (agent name): optional, specify use which agent, default=human
- r (reward function name): optional, specify use which reward function, can be zero, penalty...; default=zero
- render_image: optional: default to `False`. If used, images of current episode will be rendered into the specified path.
- render_path: optional: default to \'../assets/images/rendered/\'. A folder containing rendered images will be generated in the specified path.

For example, following parameter can run roof template with variant number 0.5, with penalty reward function, but does not generate any rendered image: 

<code> python BMApplication.py roof --v 0.5 --r penalty </code> <br>

If want to generate rendered images: 

<code> python BMApplication.py roof --v 0.5 --r penalty --render-image </code> <br>

Specifiy the path to  generate rendered images: 

<code> python BMApplication.py roof --v 0.5 --r penalty --render-image 'path/to/dir/' </code> <br>

Sample renderer output (default path):

![sample-render-output](assets/images/render-output-sample.png)



# 6: Select the interpreter from this environment:
In VSCode, you can choose your interpreter to be this conda environment by having the Python Extension installed and by opening the command pallette and selecting 'select interpreter'. <br>
You can also use the command palette to create a new python terminal, which automaticlaly activates the selected conda environment!