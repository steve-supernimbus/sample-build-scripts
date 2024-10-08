LaunchFleet Script
The LaunchFleet.py script creates a new GameLift build and then creates a new fleet using the provided arguments. 

Once the fleets are ready, it will write the new fleet’s id to disk on the agent. 

We only utilise this script in the nightly build pipeline. 

The script arguments are described below:
--build_name
This is a string arg that lets you set the name of the build that will be uploaded to GameLift.
--build_version
This is a string arg that lets you set the version of the uploaded build.
--build_path
This is a string arg that lets you set the “build_path” where your server build is located on the agent disk. The script will also take the server’s launch path from this local directory.
--build_sdk_version
This is a string arg that lets you set the version of the GameLift server SDK that is used in the build. Without this arg, GameLift will default to the wrong version by default.
--fleet_name
This is a string arg that lets you name the new fleet.
--aws_region
This is a string arg that sets the fleet’s home region.
