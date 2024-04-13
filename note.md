1. **Pre-Action Item Check for Place**: Before executing a 'Place' action, the previous action must be carrying the item specified in the 'items'. If the 'items' attribute is empty or contains a different item, the 'Place' action is invalid.

2. **Pre-Action Item Check for Pick**: Before executing a 'Pick' action, the 'items' attribute of previous action should be empty.

3. **Environment Consistency for Pick, Place and Done**: The 'environment' attribute precedes a 'Pick' or 'Place' or 'Done' action must be matched. If there is a mismatch, the sequence is invalid.

4. **Done Resets State**: After a 'Done' action, the robot should be ready to execute any valid action sequence. it can't directly follow by another 'Done' action and it should at the same environment and with proper items condition if want to perform the pick or place.

5. **No Consecutive Goto to the Same Place**: Two consecutive 'Goto' actions to the same place are unnecessary and should be optimized out.

6. **Go to Place Constraint**: Any action precedes the goto command need to ensure the they carry the required item that goto command needs, the preceded action can carry the items the later command don't need.
