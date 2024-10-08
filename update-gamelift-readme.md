UpdateGameLift Script
The UpdateGameLift.py script is used in the GameLiftTutorial_GameLift_Polling pipeline to first poll a specific fleet id to make sure it activates correctly. 

If the fleet is Active, it updates the provided alias to point at the new fleet that was activated. If the fleet is configured to launch in multiple regions, the alias will only be switched if all regions activate successfully. This avoids pointing an alias at a fleet that is in the error state. 

This script does not make any decisions about deleting old fleets, so you’ll need to make sure you clean up old or unused fleets. 

The script arguments are described below:
--alias_id
This is a string arg that sets the alias id to be updated on successful activation.
--fleet_id
This is a string arg that sets the new fleet to be polled for activation.
--monitoring_interval
This is an int arg that lets you set the number of seconds to wait in between polling the fleet’s state. Activations tend to take upwards of 30 minutes. A 60-second interval is frequent enough in most scenarios.
--timeout
This is an int arg that lets you configure a polling timeout. It defaults to 3600 seconds which translates to an hour.
