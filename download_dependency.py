#! python3

import os
import sys
import argparse
import yaml

parser = argparse.ArgumentParser(description='This program can download the third-party modules contained in this library', usage='Scattered dependent file management script')
parser.add_argument('-m', '--module', dest='module', type=str,nargs='*', help='Select the module to enable')
args = parser.parse_args()

if args.module != None:
    enable_modules = args.module

pwd = os.getcwd()

yaml_file = 'modules.yaml'
temp_dir = 'tmp'

def read_conf(file):
    fs = open(file,'r',encoding='utf-8')
    datas = yaml.load(fs,Loader=yaml.SafeLoader) 
    return datas

def processing(module,conf):
    if args.module != None and module not in enable_modules:
        print(f'I: Module {module} is not enabled, skip')
        return None
    if 'type' not in conf:
        print(f'E: Module {module} is missing the type field, skip')
        return
    if 'mode' not in conf:
        print(f'E: Module {module} is missing the mode field, skip')
        return
    type = conf['type']
    mode = conf['mode']
    print(f'I: {module} is the {type} type')
    print(f'I: {module} uses {mode} method to obtain')
    if mode == 'git_repo':
        if 'git_repo' not in conf:
            print(f'E: Module {module} is missing the download git_repo field, skip')
            return
        if 'paths' not in conf:
            print(f'E: Module {module} is missing the download paths field, skip')
            return
        repo = conf['git_repo']
        paths = conf['paths']
        print(f'I: Module {module} performs cloning {pwd}/{temp_dir}/{type}/{module}')
        if os.system(f'git clone --recurse-submodules {repo} {pwd}/{temp_dir}/{type}/{module}'):
            print(f'E: Module {module} Execution command error, termination')
            sys.exit(1)
        else:
            if type == 'modules':
                full_src_path = f'{pwd}/{temp_dir}/{type}/{module}/*'
                full_dest_path = f'{pwd}/{type}/{module}/'
                print(f'I: Module {module} copy {full_src_path} to {full_dest_path} ')
                if os.system(f'mkdir -p {full_dest_path} && cp -r {full_src_path} {full_dest_path}'):
                    print(f'E: Module {module} Execution command error, termination')
                    sys.exit(1)
            else:
                print(f'E: Modules {module} not support {type} type')
                sys.exit(1)
    elif mode == 'wget':
        if 'wget' not in conf:
            print(f'E: Module {module} is missing the download wget field, skip')
            return
        if 'filename' not in conf:
            print(f'E: Module {module} is missing the download filename field, skip')
            return
        if 'dest' not in conf:
            print(f'E: Module {module} is missing the download dest field, skip')
            return
        download_url = conf['wget']
        filename = conf['filename']
        desk_file = conf['dest']
        print(f'I: Module {module} performs download {pwd}/{temp_dir}/{type}/{filename}')
        if os.system(f'wget {download_url} -P {pwd}/{temp_dir}/{type}'):
            print(f'E: Module {module} Execution command error, termination')
            sys.exit(1)
        else:
            print(f'Module {module} Start unpacking Tar.gz')
            if os.system(f'mkdir -p {pwd}/{temp_dir}/{type}/{module} && tar xvf {pwd}/{temp_dir}/{type}/{filename} -C {pwd}/{temp_dir}/{type}/{module}'):
                print(f'E: Module {module} Execution command error, termination')
                sys.exit(1)
            if type == 'depends':
                full_src_path = f'{pwd}/{temp_dir}/{type}/{module}'
                full_dest_path = f'{pwd}/{desk_file}/{type}/{module}'
                print(f'I: Module {module} copy {full_src_path} to {full_dest_path} ')
                if os.system(f'mkdir -p {full_dest_path} && cp -r {full_src_path} {full_dest_path}'):
                        print(f'E: Module {module} Execution command error, termination')
                        sys.exit(1)
            else:
                print(f'E: Modules {module} not support {type} type')
                sys.exit(1)
if __name__ == '__main__':
    print('I: Check the temporary folder')
    if not os.path.exists(f'{pwd}/{temp_dir}'):
        print('I: Temporary folder does not exist, create now')
        os.mkdir(f'{pwd}/{temp_dir}')
        print('I: Temporary folder does not exist, creation' + f' {pwd}/{temp_dir}' + ' is complete')
        print('I: Check the temporary modules folder')
        if not os.path.exists(f'{pwd}/{temp_dir}/modules'):
            print('I: Temporary modules folder does not exist, create now')
            os.mkdir(f'{pwd}/{temp_dir}/modules')
            print('I: Temporary modules folder does not exist, creation' + f' {pwd}/{temp_dir}/modules' + ' is complete')
        print('I: Check the temporary depend folder')
        if not os.path.exists(f'{pwd}/{temp_dir}/depend'):
            print('I: Temporary depend folder does not exist, create now')
            os.mkdir(f'{pwd}/{temp_dir}/depend')
            print('I: Temporary depend folder does not exist, creation' + f' {pwd}/{temp_dir}/depend' + ' is complete')
        
    yaml_data = read_conf(f'{pwd}/{yaml_file}')
    if yaml_data:
        for module,conf in yaml_data.items():
            print(f'I: Start processing {module} module')
            processing(module,conf)
            print(f'I: Module {module} is processed')
