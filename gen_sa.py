# Created by kichappa on 12 May 2021
# A tool to create Google service accounts.


import argparse
import os

from google.oauth2 import service_account
import googleapiclient.discovery
from random import choice
from base64 import b64decode
from json import dumps, dump, loads, load
import pathlib
import ast
from math import remainder
from time import sleep
import argparse


# kichapp: Create a project, setup oAuth Client and credentials (desktop app). Now, create a service account for that and create keys for it. Download the key file and paste it in the "accounts" folder. Paste its filename in the end here.   
# google_app_cred = str(pathlib.Path().absolute())+"\\"+"python-controller.json"
google_app_cred = str(pathlib.Path().absolute())+"\\"+"credentials.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_app_cred

def _list_projects():
    """Creates a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
        
    service = googleapiclient.discovery.build(
        'cloudresourcemanager', 'v1', credentials=credentials)
    
    return service.projects().list().execute()
    # return [i['projectId'] for i in service.projects().list().execute()['projects']]

def list_keys(service_account_email):
    """Lists all keys for a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    keys = service.projects().serviceAccounts().keys().list(
        name='projects/-/serviceAccounts/' + service_account_email).execute()

    return [key['name'] for key in keys['keys']]

def delete_key(full_key_name):
    """Deletes a service account key."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    service.projects().serviceAccounts().keys().delete(
        name=full_key_name).execute()

    # print('Deleted key: ' + full_key_name)

def create_service_account(project_id, name, display_name):
    """Creates a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    my_service_account = service.projects().serviceAccounts().create(
        name='projects/' + project_id,
        body={
            'accountId': name,
            'serviceAccount': {
                'displayName': display_name
            }
        }).execute()

    print('Created service account: ' + my_service_account['email'])
    return my_service_account

def list_service_accounts(project_id):
    """Lists all service accounts for the current project."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    service_accounts = service.projects().serviceAccounts().list(
        name='projects/' + project_id, pageSize=100).execute()

    # for account in service_accounts['accounts']:
    #     print('Name: ' + account['name'])
    #     print('Email: ' + account['email'])
    #     print(' ')
    return service_accounts

def _generate_id(prefix='saf-'):
    chars = '-abcdefghijklmnopqrstuvwxyz1234567890'
    return prefix + ''.join(choice(chars) for _ in range(25)) + choice(chars[1:])

def _list_sas(iam,project):
    resp = iam.projects().serviceAccounts().list(name='projects/' + project,pageSize=100).execute()
    if 'accounts' in resp:
        return resp['accounts']
    return []

def create_key(service_account_email):
    """Creates a key for a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    key = service.projects().serviceAccounts().keys().create(
        name='projects/-/serviceAccounts/' + service_account_email, body={}
        ).execute()

    # print('Created key: ' + key['name'])
    return key

# # print(sa_created)
# # print(list_service_accounts(project_id))

# sleep_time=10
# sleep(sleep_time)


def _create_sas(project_id, prefix, count):
    sa_created=[]
    for sas_index in range(count):
        name=_generate_id(prefix)
        sa_created.append(create_service_account(project_id, name, name))
    return sa_created

def _generate_keys(project_id, prefix):
    total_sas = list_service_accounts(project_id)['accounts']
    prefix_sas=[]
    print("Length of sas =", len(total_sas))
    for account in total_sas:
        # print("%s, prefix=%s" %(account['displayName'],account['displayName'][0:3]))
        if(account['displayName'][0:len(prefix)]==prefix):
            prefix_sas.append(account)

    print("Length of {} sas =".format(prefix), len(prefix_sas))

    i=0
    sas_list_string = ""
    if not os.path.isdir('%s\\accounts\\' % pathlib.Path().absolute()):
        os.mkdir('%s\\accounts\\' % pathlib.Path().absolute())
    sas_list = open('%s\\accounts\\sas-list.txt' % pathlib.Path().absolute(), 'w+')
    sas_list.close()
    for sas in prefix_sas:
        sas_list = open('%s\\accounts\\sas-list.txt' % pathlib.Path().absolute(), 'a')
        sas_list_string+=str(sas['email'])+"\n"
        # print(i)
        if (remainder(i,10)==-1):
            sas_list_string+="\n"
            i=0
        else:
            i+=1
        sas_list.write(sas_list_string)
        sas_list_string = ""
        response = create_key(sas['email'])
        # print("\n\n\n",response['privateKeyData'],"\n\n\n")
        key_dump = {"name":response['name'][response['name'].rfind('/'):], "data":ast.literal_eval(b64decode(response['privateKeyData']).decode('utf-8'))}
        # print(key_dump["data"])
        with open('%s\\accounts\\%s.json' % (pathlib.Path().absolute(),key_dump["name"]), 'w+') as f:
            f.write(dumps(key_dump['data'], indent = 2))

def _list_sas(project_id, prefix=""):
    total_sas = list_service_accounts(project_id)['accounts']
    if not prefix=="":
        prefix_sas=[]
        for account in total_sas:
            if(account['displayName'][0:len(prefix)]==prefix):
                prefix_sas.append(account)
        total_sas=prefix_sas
    return[sas['email'] for sas in total_sas]

def _list_sas_keys(total_sas, prefix=""):
    # if not prefix=="":
    #     prefix_sas=[]
    #     for account in total_sas:
    #         if(account['displayName'][0:len(prefix)]==prefix):
    #             prefix_sas.append(account)
    #     total_sas=prefix_sas
    key_names=[]
    for sas in total_sas:
        keys=list_keys(sas)
        for key in keys:
            key_names.append(key)
        # print(sas)
        # print(list_keys(sas))
    return key_names

def _delete_keys(key_names):
    for key in key_names:
        try:
            delete_key(key)
        except:
            pass
            # print("skipping key {}".format(key))

def _delete_sas_keys(project_id, prefix=""):
    _delete_keys(_list_sas_keys(_list_sas(project_id, prefix=prefix)))

if __name__ == '__main__':

    # TODO: replace with your project ID
    # project_id = "pid"

    #argument parser
    parser=argparse.ArgumentParser(description="A tool to create Google service accounts.")
    parser.add_argument('--create-sas', action="store_true", help='create service accounts.')
    parser.add_argument('-pid', '--proj-id', type=str, help="the name id of the project.")
    parser.add_argument('-sp', '--sas-prefix', default='', help="the prefix to the name(s) of the service accounts.")
    parser.add_argument('-sc', '--sas-count', type=int, default=99, help="the number of service accounts to be created.")
    parser.add_argument('--list-projects', action="store_true", help="list projects in Google cloud.")
    parser.add_argument('--list-sas', action="store_true", help="list sas in Google cloud.")
    parser.add_argument('--generate-keys', action="store_true", help='generate keys for prefixed service accounts')    
    parser.add_argument('--delete-sas-keys', action="store_true", help='delete all keys for prefixed service accounts')
    args = parser.parse_args()

    if args.create_sas:
        if args.sas_prefix=='':
            print("Creating {} sas under the project \"{}\" without any prefix.".format(args.sas_count, args.proj_id))
        else:
            print("Creating {} sas under the project \"{}\" with a prefix \"{}\".".format(args.sas_count, args.proj_id, args.sas_prefix))
        _create_sas(args.proj_id, args.sas_prefix, args.sas_count)
    elif args.list_projects:
        print("Your projects:\n", _list_projects())
    elif args.generate_keys:        
        if args.sas_prefix=='':
            print("Creating keys for sas under the project \"{}\" without prefix filtering.".format(args.proj_id))
        else:
            print("Creating keys for sas under the project \"{}\" with a prefix \"{}\".".format(args.proj_id, args.sas_prefix))
        _generate_keys(args.proj_id, args.sas_prefix)
    elif args.list_sas:
        if args.sas_prefix=='':
            print("Listing sas that are under the project \"{}\".".format(args.proj_id))
        else:
            print("Listing sas that are under the project \"{}\" with a prefix \"{}\".".format(args.proj_id, args.sas_prefix))
        print(*_list_sas(args.proj_id, args.sas_prefix), sep='\n')
    if args.create_sas:
        if args.sas_prefix=='':
            print("Deleting all sas keys under the project \"{}\" without any prefix filtering.".format(args.proj_id))
        else:
            print("Deleting all sas keys under the project \"{}\" with a prefix \"{}\"".format(args.proj_id, args.sas_prefix))
        _delete_keys(_list_sas_keys(_list_sas(args.proj_id, args.sas_prefix)))


    # kichappa: Use functions as required
    # _create_sas(project_id, pref, 99)
    # _generate_keys(project_id, prefix='mfc-')
    # print(_list_projects())
    # print(_list_sas_keys(_list_sas(project_id=project_id, prefix="mfc-")))
    # _delete_keys(_list_sas_keys(_list_sas(project_id=project_id, prefix="mfc-")))

