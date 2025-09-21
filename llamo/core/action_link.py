def ActionLink(action1, action2):
    # Rule 1: Pre-Action Item Check for Place
    action1_item = list(action1.values())[0]["items"]
    action2_item = list(action2.values())[0]["items"]
    action1_env = list(action1.values())[0]["environment"]
    action2_env = list(action2.values())[0]["environment"]
    
    if action1.get("Done"):
        print(1)
    
    if action2.get("Place") and (action1_item != action2["Place"]["Parameter"]):
        return (False, "Don't bring require item for place cmd")
    

    if action1.get('Done') and action2.get("Pick"):
        if len(list(action1.values())[0]["environment_items"])>0:
            if list(action1.values())[0]["environment_items"][0] == action2['Pick']['Parameter']:
                return (True, "")

    # Rule 2: Pre-Action Item Check for Pick
    if action2.get("Pick") and action1_item != "":
        return (False, "bring item before picking")

    # Rule 3: Environment Consistency for Pick, Place and Done
    if action2.get("Pick") or action2.get("Place") or action2.get("Done"):
        if action1_env != action2_env:
            return (False, "Envs are not consist")

    # Rule 4: Done constraint
    if action2.get("Done"):
        return False, "Can't follow done"

    # Rule 5: No Consecutive Goto to the Same Place
    # if (
    #     action1.get("Goto")
    #     and action2.get("Goto")
    #     and action1["Goto"]["Parameter"] == action2["Goto"]["Parameter"]
    # ):
    #     return (False, "Can't go the same place")


    # Rule 6: Go to Place Constraint
    if action2.get("Goto"):
        required_item = list(action2.values())[0]["items"]
        if required_item != action1_item:
            return (False, "Items are not match for goto cmd")
        # if action1_env == action2["Goto"]["Parameter"]:  # if already at the place
        #     return (False, "It already at the place")

    return (True, "")


if __name__ == "__main__":
    input = [
        {"Goto": {"Parameter": "table2", "items": "", "environment": "table2"}},
        {"Pick": {"Parameter": "pencil", "items": "pencil", "environment": "table2"}},
        {"Goto": {"Parameter": "table1", "items": "pencil", "environment": "table1"}},
        {"Place": {"Parameter": "pencil", "items": "", "environment": "table1"}},
        {"Done": {"Parameter": "", "items": "", "environment": "table1"}},
    ]
    candidates = [
        {"Goto": {"Parameter": "table1", "items": "", "environment": "table1"}},
        {"Pick": {"Parameter": "box", "items": "box", "environment": "table1"}},
        {"Goto": {"Parameter": "table2", "items": "box", "environment": "table2"}},
        {"Place": {"Parameter": "box", "items": "", "environment": "table2"}},
        {"Goto": {"Parameter": "table1", "items": "", "environment": "table1"}},
        {"Pick": {"Parameter": "rubber", "items": "rubber", "environment": "table1"}},
        {"Goto": {"Parameter": "table2", "items": "rubber", "environment": "table2"}},
        {"Place": {"Parameter": "rubber", "items": "", "environment": "table2"}},
        {"Done": {"Parameter": "", "items": "", "environment": "table2"}},
    ]
    for i in input:
        for candidate in candidates:
            result = ActionLink(i, candidate)
            print(i)
            print(candidate)
            print(result)
            print("-"*10)
