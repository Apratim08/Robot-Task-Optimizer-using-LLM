            [Tasks]
            Move the yellow box from the white table to the gray table
            [Environment]
            Unknown
            [Robot Information]
            Unkown
            
            [output]
            [
                {
                    "Goto":{
                        "Parameter":"white table",
                        "items":[]
                    }
                },
                {
                    "Pick":{
                        "Parameter":"yellow box",
                        "items":["yellow box"]
                    }
                },
                {
                    "Goto":{
                        "Parameter":"grey table",
                        "items":["yellow box"]
                    }
                },
                {
                    "Place":{
                        "Parameter":"yellow box",
                        "items":[]
                    }
                },
                {
                    "Done":{
                        "Parameter":"",
                        "items":[]
                    }
                }
            ]

            [Tasks]
            Go to desk to pick up a cup of coffee
            [Environment]
            Desk has rubber, ball and coffee on it.
            [Robot Information]
            Unknown
            [output]
            [
                {
                    "Goto": {
                        "Parameter": "desk",
                        "items": []
                    }
                },
                {
                    "Pick": {
                        "Parameter": "coffee",
                        "items": ["coffee"]
                    }
                },
                {
                    "Done": {
                        "Parameter": "",
                        "items": []
                    } 
                }
            ]
            
            [Tasks]
            Go from bedroom to living room to pick up a cup
            [Environment]
            bedroom is linked to the front_aisle, a living room is linked to the end_aisle, a cup is on the living room
            [Robot Information]
            Unknown
            [output]
            [
                {
                    "Goto": {
                        "Parameter": "front_aisle",
                        "items": []
                    }
                },
                {
                    "Goto": {
                        "Parameter": "end_aisle",
                        "items": []
                    }
                },
                {
                    "Goto": {
                        "Parameter": "living room",
                        "items": []
                    }
                },
                {
                    "Pick": {
                        "Parameter": "cup",
                        "items": ["cup"]
                    }
                },
                {
                    "Done": {
                        "Parameter": "",
                        "items": []
                    }
                }
            ]
        Output MUST be purely python list.
        """