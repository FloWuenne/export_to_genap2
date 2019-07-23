
import sys, os
import argparse
import os.path
import re
import shutil



def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_dir', help='Base dir', required=True)
    parser.add_argument('-e', '--user_email', help='Galaxy email_user_name', required=True)
    parser.add_argument('-d', '--dataset', help='A unique and representative name to your dataset which will be seen in the shiny app',required=True)
    parser.add_argument('-c', '--clustering_file', help='Feather file containing clustering results', required=True)
    parser.add_argument('-g', '--gene_names', help='Gene names for feather file', required=True)
    parser.add_argument('-u', '--user_clustering', help='User cluster annotation', required=True)
    parser.add_argument('-s', '--clustering_sparse', help='Full expression data in sparseMatrix format', required=True)

    return parser.parse_args()


def create_user_dir(user, base_dir, dataset):

    dir_full_path = os.path.join(base_dir,os.path.join(user, dataset))

    if not os.path.exists(base_dir):
        raise Exception("'%s' directory does not exist or it is not accessible by the Galaxy user" % base_dir)

    # Create user dir
    try: 
        os.makedirs(dir_full_path)
    except OSError:
        if not os.path.isdir(dir_full_path):
            raise

    return dir_full_path


def copy_data(dir_full_path, files):

    exit_code = 0
    for file in files:
        try:
            shutil.copy2(file, dir_full_path)
            print("Dataset '%s' copied to '%s'" % (file, dir_full_path))
        except Exception as e:
            msg = "Error copying dataset '%s' to '%s', %s" % (file, dir_full_path, e)
            print(msg)
            exit_code = 1

    return exit_code



def main():
    args = parse_command_line()
    user_name = args.user_email.split('@')

    dir_full_path = create_user_dir(user_name[0], args.base_dir,args.dataset)

    exit_code = copy_data(dir_full_path, [args.clustering_file, args.gene_names, args.user_clustering,  args.clustering_sparse])

    sys.exit(exit_code)


if __name__ == "__main__" :
    main()





    
   