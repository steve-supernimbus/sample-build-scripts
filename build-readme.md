# Build Sample Script
The script “Build.py” allows you to build your Unreal Engine 5 project. You can customise your build’s configuration, target platforms for both the client and server, and whether to build prerequisites for the client, the server or both.

## Arguments:
### --pre_reqs
This is a bool argument that decides if pre-requisite engine components will be installed. It will build the Unreal Engine Editor, the shader compile worker for the provided configuration and the project’s Development Editor. Defaults to False.

### --client
This is a bool argument that decides if a client will be built and packaged. If true it will also build the client target for the provided configuration. Defaults to False.

### --server
This is a bool argument that decides if a server will be built and packaged. If true it will also build the server target for the provided configuration. Defaults to False.

### --client_target
This is a string argument that lets you set the client’s target platform. Defaults to Win64.

### --server_target
This is a string argument that lets you set the server’s target platform. Defaults to Win64.

### --configuration
This is a string argument that lets you set the target configuration for the build. Defaults to Development.
