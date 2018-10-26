#!/usr/bin/python 
import os
import os.path
import config

def _walk_dir_get_files(dir):
    for parent,child_dirs,child_files in os.walk(dir):        
        for file in child_files:
            file_full_path = os.path.normpath(os.path.join(parent,file))
            yield file_full_path.replace('\\','/').replace('lfs-commands/','')

def gen_make_item(item , last_target, shell_path):
    target = ''
    dep = last_target
    pkg = ''
    tpl = ''
    if 'target' in item: target = item['target']
    if 'dep' in  item: dep = item['dep']
    if 'pkg' in  item: pkg = item['pkg']
    if 'tpl' in  item: tpl = item['tpl']
    if target == '' or tpl == '' :
        print('config error, item:', item)
        exit()
    if  tpl not in config.make_cmd_tpl_map:
        print('tpl invalid,item:', item)
        exit()
    return config.make_cmd_tpl_map[tpl].\
              replace('__TARGET__',target).\
              replace('__DEP__',dep).\
              replace('__PKG_NAME__',pkg).\
              replace('__TARGET_SHELL__',shell_path).\
              replace('__NAME_FORM_TARGET__',target)

def gen_makefile():
    last_target = ""
    dep_details_content = ""
    cmd2path = {'LUSER_BEGIN':'','LUSER_END':'','SUDO_BEGIN':'','SUDO_END':'','CHROOT_BEGIN':'',\
                'CHROOT_END':'','BOOT_BEGIN':'','BOOT_END':'','CUSTOM_BEGIN':'','CUSTOM_END':''}
    for path in _walk_dir_get_files('./lfs-commands'):
        cmd2path[os.path.basename(path)] = path
    for item in config.dep_details:
        target = item['target']
        if target not in cmd2path:
            print('can not find make command for ', item)
            exit()
        dep_details_content += '\n'
        dep_details_content += gen_make_item(item , last_target, cmd2path[target])
        last_target = target

    makefile =  open('Makefile.tpl').read().\
              replace('__VAR_DEF_TPL__' , config.var_def).\
              replace('__STAGE_GROUP_TPL__' , config.stage_group).\
              replace('__DEP_DETAILS_TPL__' , dep_details_content) 
    with open('Makefile' , 'w') as out:
        out.write(makefile)        

if __name__ == "__main__":
   os.system('bash check_host_reqs.sh')
   gen_makefile()
   print('gen makefile succ')