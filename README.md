**Personal timeline python script**

This script will trigger a reminder mail to our inbox based on the timeline/event added in datesData.txt

_Requirements_:

User need registered gmail mail id to get <client-id>, <secret-id>, <client-secret> json from google.cloud.console to access gmail api
  
Download and save it the same working directory as credentials.json
  
The script will ask for providing access for the project to access your gmail
  
If the token expires need to provide access again, this can be avoided by creating a refresh token.
  
Using the refresh token to get authorization token if the token expires. (todo: not updated in this script)
