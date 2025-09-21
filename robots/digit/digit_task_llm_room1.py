import asyncio

import agility
import agility.messages as msgs

import numpy as np
import re

from llm import llm_init, llm_query



def set_box_polygon(box_geometry):
    '''
    This function transforms the geometry of a box into the keep-out zone polygon
    Parameters:
        box_geometry - Three-element list with the x, y, and z dimensions of the box
    '''
    return [
        [box_geometry[0]/2, box_geometry[1]/2],
        [box_geometry[0]/2, -box_geometry[1]/2],
        [-box_geometry[0]/2, -box_geometry[1]/2],
        [-box_geometry[0]/2, box_geometry[1]/2],
    ]

def init_msg():
    global all_msg, failure_msg, counter
    counter = 0
    all_msg = []
    failure_msg = None

def save_msg(msg):
    global all_msg, failure_msg
    msg_str = str(msg)
    all_msg.append(msg_str)

    if "action-status-changed" in msg_str and "'status': 'failure'" in msg_str:
        match = re.search(r"'info': '(.*?)'", msg_str)
        if match:
            failure_msg = match.group(1)

async def run_step(api, msg):
    global prev_map, counter
    
    # package properties
    package = {
        'geometry': [0.32, 0.28, 0.3],
        'mass': 0.1
    }

    if 'front_aisle' in msg:
        # import pdb; pdb.set_trace()
        await api.wait_action(msgs.ActionGoto(
        target=msgs.Pose(axyd=[90, 3, 0]),
        # reference_frame=msgs.ObjectSelector(map_name='wall1-map')
        ))
    
    if 'end_aisle' in msg:
        # import pdb; pdb.set_trace()
        await api.wait_action(msgs.ActionGoto(
        target=msgs.Pose(axyd=[180, 3, 4]),
        # reference_frame=msgs.ObjectSelector(map_name='wall1-map')
        ))

    if 'turn around' in msg:
    # import pdb; pdb.set_trace()
        await api.wait_action(msgs.ActionGoto(
        target=msgs.Pose(axyd=[270, 5, 5.5]),
        # reference_frame=msgs.ObjectSelector(map_name='wall1-map')
        ))
    
    # if 'room2' in msg:
    #     # import pdb; pdb.set_trace()
    #     await api.wait_action(msgs.ActionGoto(
    #     target=msgs.Pose(axyd=[180, 5.5, 5.5]),
    #     # reference_frame=msgs.ObjectSelector(map_name='wall1-map')
    #     ))
    if 'gray table' in msg:
        await api.wait_action(msgs.ActionGoto(
        target=msgs.Pose(axyd=[180, 1, 0]),
        reference_frame=msgs.ObjectSelector(map_name='table1-map')
        ))
        # await asyncio.sleep(3)
    if 'brown table' in msg:
        await api.wait_action(msgs.ActionGoto(
        target=msgs.Pose(axyd=[180, 1, 0]),
        reference_frame=msgs.ObjectSelector(map_name='table2-map')
        ))    
    if 'No. 5' in msg:
        mob = msgs.MobilityParameters()
        mob.leg_length = 1
        await api.send(msgs.ActionPick(
            {'owned-object-name': 'package-1'},mobility_parameters=mob
        ))
        await asyncio.sleep(12)
    if 'No. 7' in msg:
        mob = msgs.MobilityParameters()
        mob.leg_length = 1
        await api.send(msgs.ActionPick(
            {'owned-object-name': 'package-2'},mobility_parameters=mob
        ))
        await asyncio.sleep(12)
    if 'No. 10' in msg:
        mob = msgs.MobilityParameters()
        mob.leg_length = 1
        await api.send(msgs.ActionPick(
            {'owned-object-name': 'package-3'},mobility_parameters=mob
        ))
        await asyncio.sleep(12)

        
        # # Apply force
        # if counter <= 3:
        #     print("Apply force.")
        #     await api.send(msgs.SimulatorApplyForce(
        #         model_id=3,
        #         offset=[0,0,0],
        #         reference="body",
        #         force={"xyz":[0,-100,-200]},
        #         duration=300))
        # else:
        #     # Wait so that you can debug in the gamepad interface if needed
        #     await asyncio.sleep(3)
        #     await api.wait_action(msgs.ActionGoto(
        #     target=msgs.Pose(axyd=[0,2.5,0.0]),
        #     reference_frame=msgs.ObjectSelector(map_name=prev_map)))
            
    if 'Place' in msg and 'No. 7' in msg:
        try:
            await api.wait_action(msgs.ActionPlace(
                # position_tolerance = 0.1,
                pose=msgs.Pose(xyz=[-package['geometry'][0], 0, package['geometry'][2]]),
                reference_frame=msgs.ObjectSelector(map_name='table2-map')))
            await asyncio.sleep(3)
        except agility.exceptions.ActionFailed:
            print('action failed')
        
        
    if 'Place' in msg and 'No. 5' in msg:
        try:
            await api.wait_action(msgs.ActionPlace(
                # position_tolerance = 0.1,
                pose=msgs.Pose(xyz=[-package['geometry'][0], 0.5, package['geometry'][2]]),
                reference_frame=msgs.ObjectSelector(map_name='table2-map')))
            await asyncio.sleep(3)
        except agility.exceptions.ActionFailed:
            print('action failed')
            
    if 'Place' in msg and 'No. 9' in msg:
        try:
            await api.wait_action(msgs.ActionPlace(
                # position_tolerance = 0.1,
                pose=msgs.Pose(xyz=[-package['geometry'][0], -0.5, package['geometry'][2]]),
                reference_frame=msgs.ObjectSelector(map_name='table2-map')))
            await asyncio.sleep(3)
        except agility.exceptions.ActionFailed:
            print('action failed')
        # await api.wait_action(msgs.ActionGoto(
        #     target=msgs.Pose(axyd=[0,2.0,0.0]),
        #     reference_frame=msgs.ObjectSelector(map_name=prev_map)))
    # else:
    #     await asyncio.sleep(100)
    # await asyncio.sleep(3)

async def llm_plan(api, msg):
    global prev_map, failure_msg
    prev_map = None

    while 'Done' not in msg:
        if failure_msg != None:
            msg = "[Status] {}".format(failure_msg)
            # print(msg)
            failure_msg = None
        msg = await llm_query(msg)
        print(msg)
        await run_step(api, msg)
        await asyncio.sleep(1)
    

async def main(host_address, task):
    '''
    The main function that starts all other tasks
    Parameters:
        host_address - '10.10.1.1' to run on the robot or '127.0.0.1' to run on
        the simulator
    '''

    async with agility.JsonApi(host_address) as api:
        global prev_map, counter

     
    # table1 properties
        table1 = {
            'geometry': [0.86, 1.78, 0.05],
        }

    # table2 properties
        table2 = {
            'geometry': [0.86, 1.78, 0.05],
        }

    # package properties
        package = {
            'geometry': [0.32, 0.28, 0.3],
            'mass': 0.1,
            "fricion" : [5,5,5]
        }

        # Install default error/warning handlers that just print messages
        api.handle('all', lambda msg: save_msg(msg))

        # Request the change action command privilege
        await api.request_privilege('change-action-command')

        # Set up table 1
        await api.send(msgs.AddLandmarks(
            map_name='table1-map',
            landmarks=[
                msgs.Landmark(id=1, pose=msgs.Pose(axyzd=[0, 0.0, -0.6, 0.0])),
                msgs.Landmark(id=2, pose=msgs.Pose(axyzd=[0, 0.0, 0.6, 0.0]))
            ]
        ))

        # Add the first table and its keep out zone
        await api.get_response(msgs.AddObject(
            attributes={
                'name': 'table-1',
                'box-geometry': table1['geometry'],
                'polygon': set_box_polygon(table1['geometry']),
                'keep-out': True
            },
            transform={'xyz': [-table1['geometry'][0]/2, 0, 0]},
            relative_to={'map-name': 'table1-map'}
        ))

        # # Set up table 2
        await api.send(msgs.AddLandmarks(
            map_name='table2-map',
            landmarks=[
                msgs.Landmark(id=3, pose=msgs.Pose(axyzd=[0, 0.0, -0.6, 0.0])),
                msgs.Landmark(id=4, pose=msgs.Pose(axyzd=[0, 0.0, 0.6, 0.0]))
            ]
        ))

        # # Add the second table and its keep out zone
        await api.get_response(msgs.AddObject(
            attributes={
                'name': 'table-2',
                'box-geometry': table2['geometry'],
                'polygon': set_box_polygon(table2['geometry']),
                'keep-out': True
            },
            transform={'xyz': [-table2['geometry'][0]/2, 0, 0]},
            relative_to={'map-name': 'table2-map'}
        ))

        # # Add box
        await api.get_response(msgs.AddObject(
            attributes={
                'name': 'package-1',
                'box-geometry': package['geometry'],
                'pickable': True,
                'mass': package['mass']
            }
        ))
        # # Add rubber
        await api.get_response(msgs.AddObject(
            attributes={
                'name': 'package-2',
                'box-geometry': package['geometry'],
                'pickable': True,
                'mass': package['mass']
            }
        ))
        # # Add pencil
        await api.get_response(msgs.AddObject(
            attributes={
                'name': 'package-3',
                'box-geometry': package['geometry'],
                'pickable': True,
                'mass': package['mass']
            }
        ))
        # AprilTag on box
        await api.get_response(msgs.AddObject(
            attributes={'april-tag-id': 5},
            transform={'xy': [package['geometry'][0]/2, 0]},
            relative_to={'owned-object-name': 'package-1'}
        ))
        await api.get_response(msgs.AddObject(
            attributes={'april-tag-id': 6},
            transform={'axyd': [180, -package['geometry'][0]/2, 0]},
            relative_to={'owned-object-name': 'package-1'}
        ))
        await api.get_response(msgs.AddObject(
            attributes={'april-tag-id': 7},
            transform={'xy': [package['geometry'][0]/2, 0]},
            relative_to={'owned-object-name': 'package-2'}
        ))
        await api.get_response(msgs.AddObject(
            attributes={'april-tag-id': 8},
            transform={'axyd': [180, -package['geometry'][0]/2, 0]},
            relative_to={'owned-object-name': 'package-2'}
        ))
        await api.get_response(msgs.AddObject(
            attributes={'april-tag-id': 9},
            transform={'xy': [package['geometry'][0]/2, 0]},
            relative_to={'owned-object-name': 'package-3'}
        ))
        await api.get_response(msgs.AddObject(
            attributes={'april-tag-id': 10},
            transform={'axyd': [180, -package['geometry'][0]/2, 0]},
            relative_to={'owned-object-name': 'package-3'}
        ))
        # Wait so that you can debug in the gamepad interface if needed
        await asyncio.sleep(1)

        # Disable obstacle avoidance
        await api.send(msgs.DefaultMobilityParameters(
                mobility_parameters = {
                    'avoid-obstacles' : True
                }
        ))

        await llm_plan(api, task)
        
        # Wait so that you can debug in the gamepad interface if needed
        await asyncio.sleep(1)


if __name__ == '__main__':
    llm_init()
    init_msg()
    task =  """
    Environment: A gray table locate near front aisle and a brown table is at end_aisle. packages No. 7, No. 5 are placed on gray table. Package No. 10 is on the brown table. Robot already near gray table at start

    Task: move the package from brown table to gray table
    """

    run_on_robot = False
    if run_on_robot:
        asyncio.run(main('10.10.1.1', task))
    else:
        #  Load the world
        world = "room1.toml"
        sim_path = './ar-control-2023.01.13a'

        with agility.Simulator(sim_path, world) as sim:
            # Start running main function
            asyncio.run(main('127.0.0.1', task))
