Upload Script
The script “Upload.py” will upload files to S3. It will sync all files in a local directory to S3 so that the builds are persisted to the cloud. 

It can also generate pre-signed URLs for the newly uploaded files, which will then be written to the agent disk. This makes it easy to read them back in the Jenkins pipeline and include them in the Notification email. 

The script arguments are described below:
--bucket
This is a string arg that sets the target S3 bucket.
--local_folder
This is a string arg that sets the local folder path that contains the build artefacts. All items in this directory will be uploaded to AWS.
--remote_folder
This is a string arg that sets the item prefixes on S3. This can be useful to determine which life-cycle policy will be applied to the uploaded artefacts.
--generate_links
This is a bool arg that lets you decide whether pre-signed URLs will be generated and written to disk. This defaults to “false”.
--link_expiry
This is an int arg that lets you decide the number of seconds pre-signed URLs will be active. It will default to 172800 seconds which  is 2 days.
