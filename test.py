import argparse

if __name__ == '__main__':

    project_id = "fiery-booth-313416"

    #argument parser
    parser=argparse.ArgumentParser(description="A tool to create Google service accounts.")
    createSas=parser.add_argument_group("create service accounts.")
    createSas.add_argument('--create-sas', action="store_true")
    parser.add_argument('-pid', '--proj-id', type=str, help="the name id of the project.")
    parser.add_argument('-sp', '--sas-prefix', default='', help="the prefix to the name(s) of the service accounts to be created.")
    createSas.add_argument('-sc', '--sas-count', type=int, default=99, help="the number of service accounts to be created.")
    parser.add_argument('--list-projects', action="store_true", help="list projects in Google cloud.")
    parser.add_argument('--list-sas', action="store_true", help="list sas in Google cloud.")
    generateKeys=parser.add_argument_group("generate keys for prefixed service accounts.")
    generateKeys.add_argument('--generate-keys', action="store_true")
    args = parser.parse_args()

    if args.create_sas:
        if args.sas_prefix=='':
            print("Creating {} sas under the project \"{}\" without any prefix".format(args.sas_count, args.proj_id))
        else:
            print("Creating {} sas under the project \"{}\" with prefix \"{}\"".format(args.sas_count, args.proj_id, args.sas_prefix))
    elif args.list_projects:
        print("Listing projects")
    elif args.generate_keys:
        print("Creating keys for sas under the project \"{}\" with prefix \"{}\"".format(args.proj_id, args.sas_prefix))
    elif args.list_sas:
        if args.sas_prefix=='':
            print("Listing sas that are under the project \"{}\"".format(args.proj_id))
        else:
            print("Listing sas that are under the project \"{}\" with prefix \"{}\"".format(args.proj_id, args.sas_prefix))
    