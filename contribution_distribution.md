During the development of our benchmark we organised weekly meetings to discuss the project. We did this to keep the group informed about progress, provide an opportunity to efficiently discuss ideas and opinions, and to delegate tasks which were suited to the strengths and interests of each individual. We aimed to let eachother know when we were going ahead with a particular contribution. Each individual found themselves able to work on the project at different times. If one individual was not able to contribute at a particular time, then the others would continue with development in their stead.

Our group was not without its faults when it came to teamwork. In future, we would consider using a more rigid development framework. We could have made more use of gitlab’s ‘issue’ functionality, for exam- ple.

We list the individual contributions and ideas which we each take responsibility for:

### Lachlan Stewart

- Early benchmark concept
- Created framework using Tensorflow, Box2D and Pygame for backend
- Formulated the abstract templates as reinforcement learning environments to interface with Tensorflow 
- ‘Variant’ value concept and implementation
- Template designs
- Implemented Deep-Q and Categorical Deep-Q agents using Tensorflow
- Implemented Distribution agent
- Abstracted the observation in order to include multiple approaches
- Raycasting observation concept and implementation
- New-best-height reward concept and implementation
- Carried out experiments

### Sihan Lin

- Template designs
- Benchmark framework design & refactoring
- Abstraction of agent & formalize agent which accept human input
- Structure agent action space & movement unit
- Abstract reward function and implement basic sparse reward functions 
- Parameterized application launch arguments
- Implement efficient image observation & create DQN agent from it
- Conduct experiment on image-based DQN agent

### Xin Lu

- Proposed action tasks and early benchmark concept 
- Proposed idea of interactive physical ‘puzzle’
- Proposed idea of agents conducting ‘pushing’ actions 
- Template designs
- Implemented heuristic agent (avoidance)
- Implemented heuristic agent (pushing)
- Implemented image renderer and GIF convertor to visualize agent task performance
- Conducted experiments of heuristic agents and created quantitative graphs