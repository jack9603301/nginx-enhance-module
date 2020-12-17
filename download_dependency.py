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

print(args.module)

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
        if 'mode' not in conf:
            print(f'E: Module {module} is missing the download mode field, skip')
            return
        if 'paths' not in conf:
            print(f'E: Module {module} is missing the download paths field, skip')
            return
        repo = conf['git_repo']
        paths = conf['paths']
        print(f'I: Module {module} performs cloning {pwd}/{temp_dir}/modules/{module}')
        if os.system(f'git clone --recurse-submodules {repo} {pwd}/{temp_dir}/modules/{module}'):
            print(f'E: Module {module} Execution command error, termination')
            sys.exit(1)
        else:
            for path in paths:
                full_src_path = f'{pwd}/{temp_dir}/modules/{module}/{path}/*'
                full_dest_path = f'{pwd}/modules/{module}/'
                print(f'I: Module {module} copy {full_src_path} to {full_dest_path} ')
                if os.system(f'mkdir -p {full_dest_path} && cp -r {full_src_path} {full_dest_path}'):
                    print(f'E: Module {module} Execution command error, termination')
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
        
    yaml_data = read_conf(f'{pwd}/{yaml_file}')
    if yaml_data:
        for module,conf in yaml_data.items():
            print(f'I: Start processing {module} module')
            processing(module,conf)
            print(f'I: Module {module} is processed')
