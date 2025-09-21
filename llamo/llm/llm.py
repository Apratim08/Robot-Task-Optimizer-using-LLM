import asyncio
import openai
import textwrap


def llm_init():
    #TODO add api key or use .ENV file
    openai.api_key = ''

    global prompt_system, prompt_history

    prompt_system = '''
You are a planner for a robot. Your output MUST be one of the following format:
* Go to {somewhere}
* Pick {something}
* Place {something}
* Done
    

Environment: Unknown
Task: Move the yellow box from the white table to the gray table
1. Go to the white table
2. Pick the yellow box
3. Go to the gray table
4. Place the yellow box
5. Done

Environment: Unknown
Task: Move the yellow box from the white table to the gray table
1. Go to the white table
[Status] not near the white table.
2. Go to the white table
3. Pick the yellow box
4. Go to the gray table
5. Place the yellow box
6. Done
    
Environment: Unknown
Task:   Go forward
1. Go forward
2. Done
  
Environment: Unknown
Task: Turn left
1. Turn left
2. Done
    
Environment: Unknown
Task: Turn left
1. Turn left
[Status] Not turning left
2. Turn left
3. Done
    
Environment: Unknown
Task: Turn right
1. Turn right
2. Done

Environment: bedroom is linked to the front_aisle, a living room is linked to the end_aisle, a cup is on the living room
Task: Go from bedroom to living room to pick up a cup
1. Go to the front_aisle
2. Go to the end_aisle
3. Go to the living room
4. Pick the cup

    '''
    prompt_system = textwrap.dedent(prompt_system)
    prompt_system = prompt_system.split('\n', 1)[1]

    prompt_history = ''

async def llm_query(msg):
    global prompt_system, prompt_history

    prompt_history = prompt_history + msg + '\n'

    loop = asyncio.get_event_loop()
    completion = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(
        model= "gpt-4",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_history}
        ]
    ))

    res = completion.choices[0].message.content
    res = res.split('\n', 1)[0]

    return res

def llm_test():
    msg = 'Task: Move the package from the gray table to the brown table'
    while 'Done' not in msg:
        msg = llm_query(msg)
        print(msg)

if __name__ == '__main__':
    llm_init()
    llm_test()
