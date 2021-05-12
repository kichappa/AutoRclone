from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import os, pathlib

google_app_cred = str(pathlib.Path().absolute())+"\\"+"python-controller.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_app_cred

credentials = GoogleCredentials.get_application_default()

service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

my_projects = service.projects().list().execute()
print(my_projects)
# while True:
#     request = service.projects().list()
#     response = request.execute()

#     for project in response.get('projects', []):
#         # TODO: Change code below to process each `project` resource:
#         pprint(project)

#     request = service.projects().list_next(previous_request=request, previous_response=response)