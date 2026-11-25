'''
This is the helper script for QTRIPSTATIC
It can:
1. Download the assets folder from Google Drive and untar it
2. Update the Module Id in metadata.json and push it to the git repo

Invocation:
> python3 helper.py --setup
> python3 helper.py --update <next_module_name>
'''

import argparse
import tarfile
import os
import fileinput
import re
import git
from git import Repo

def download_assets():
    print('Beginning assets download')
    os.system('wget "https://drive.google.com/uc?export=download&id=1gJ-g7EWreZu38DlaZltLDylPIBDHLSxX" -O assets.tar')
    print('Untarring assets')
    tar_file = tarfile.open('assets.tar')
    tar_file.extractall('.')
    tar_file.close()
    os.remove('assets.tar')
    print('Done')

def update_metadata(next_module_name):
    print('Updating metadata.json with module name: ', next_module_name)
    new_name = 'ME_QTRIPSTATIC_MODULE_'+next_module_name
    for line in fileinput.input(files ='__CRIO__/metadata.json', inplace=1):
        line = re.sub(r'ME_QTRIPSTATIC_MODULE_[A-Z,_]+',new_name, line.rstrip())
        print(line)
    print('Done')

def push_to_repo(next_module_name):
    print('Pushing files to git repo')
    repo = git.Repo('.')
    repo.index.add(['__CRIO__/metadata.json'])
    repo.index.commit('Update module name to '+next_module_name)
    repo.remotes.origin.push()
    print('Done')
    
def download_assets():
    import gdown

    print('Beginning assets download')

    # Always use the folder where helper.py is located
    project_dir = os.path.dirname(os.path.abspath(__file__))
    assets_path = os.path.join(project_dir, 'assets.tar')

    # Download from Google Drive
    file_id = '1gJ-g7EWreZu38DlaZltLDylPIBDHLSxX'

    downloaded_file = gdown.download(
        id=file_id,
        output=assets_path,
        quiet=False
    )

    # Check whether download was successful
    if not downloaded_file or not os.path.exists(assets_path):
        raise RuntimeError('Assets download failed!')

    print('Download completed successfully.')
    print('Untarring assets...')

    # Extract into the local project directory
    with tarfile.open(assets_path, 'r:*') as tar_file:
        tar_file.extractall(
            path=project_dir,
            filter='data'
        )

    # Remove archive after successful extraction
    os.remove(assets_path)

    print('Assets downloaded and extracted successfully!')
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--setup', help='Setup required assets', action='store_true')
    parser.add_argument('-u', '--update', help='Update the module name in metadata.json')

    args = parser.parse_args()

    if args.setup:
        download_assets()

    if args.update:
        update_metadata(args.update)
        push_to_repo(args.update)
        
        

