def filter(final_actions):
    filtered_actions = []
    for i,action in enumerate(final_actions):
        if action == "start":
            continue
        if  action.get("Done"):
            if final_actions[i - 1].get("Goto") and len(final_actions)>3 and i >2:
                # -1 for removing start
                done_index = final_actions[i -2]
                pre_index = final_actions[i - 1]
                if (
                    list(pre_index.values())[0]["environment"]
                    == list(done_index.values())[0]["environment"]
                ):
                    filtered_actions = filtered_actions[:-1]

            continue

        action_cmd = list(action.keys())[0]
        filtered_actions.append((action_cmd, action[action_cmd]["Parameter"]))

    filtered_actions +=["Done"]

    return filtered_actions
