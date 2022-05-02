# Meeting minutes

## Team Meeting 1 - Week 8 - 2022/04/26 8pm - 9:30pm

**Absent:** N\A
<br></br>
**Lead/scribe:** Xin Lu

## Agreed Procedure

- Discuss agenda
- Assign tasks
- Questions for Alex

## Agenda Items

| Number |                           Item |
| :----- | -----------------------------: |
| 1      |             Set up Gitlab repo |
| 2      |  Disucss template tasks design |
| 3      | Discuss reinforcement learning |
| 4      |         Discuss implementation |

## Meeting Minutes

- We agree that if an reinforcement learning agent can sucessfully complete a certain intuitive physic reasoning task, then we can say this agent can be considered as equivalently as an agent that understands the physic laws required to complete the task.
  - But an agent that understands the physic laws required to complete the task should be able to generalize.
- Two sets of task templates: avoiding task and puzzle task.
  - Agent embedded in the testing scenario, so it can influence the environment dynamics, and can be influenced by environment dynamics as well
  - Avoiding task and puzzle task should use a shared reward functions
  - Avoiding task and puzzle task should share the same environment setting but with different objects and goals involved
  - Avoiding task: contionusly changing rewards, goal to reach the top, agent as observer and gravity does not apply to the agent
  - Puzzle task: reward function TBD, extended PHYRE tasks, multiple action needed, clearly specified goal
- If can't decide a best-matching rewards, consider training multiple reward functions at the same time. (off-policy or on-policy)
- We may start wih a random agent, and improve it during the trail-and-error learning process.
- Questions:
  - Can we train two agents with almost identical model but only different expression for reward functions, in order to test them by different types of templates (avoiding task and puzzle task)?
  - How to train the visual encoder and decoder?
- Mentioned resources:
  - https://www.section.io/engineering-education/building-a-reinforcement-learning-environment-using-openai-gym/
  - https://openai.com/blog/faulty-reward-functions/
  - https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

## TODO Items

| Task                                                         | Assignee |
| :----------------------------------------------------------- | -------: |
| Research code implementation: Box2D, OpenAI, PyTorch etc. Focus on how to set up testing enviroment, and what are the type of inputs fed into the agent. |    Sihan |
| Design reward functions for avoding tasks                    |  Lachlan |
| Design reward functions for puzzle tasks                     |      Xin |

## Scribe Rotation

The following dictates who will be scribe in this and the next meeting. (Alphabetical order)

|  Name   |
| :-----: |
|   Xin   |
|  Sihan  |
| Lachlan |

