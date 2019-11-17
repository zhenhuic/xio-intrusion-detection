import os
import shutil
import compileall


def build_deployment(proj_root: str, deploy: str, ignores: list):
    proj_root = os.path.abspath(proj_root)
    deploy = os.path.abspath(deploy)

    compileall.compile_dir(proj_root, force=True)
    print('proj_root', proj_root)
    print('deploy', deploy)

    for root, dirs, files in os.walk(proj_root):
        ignore_flag = False
        for ign in ignores:
            if root.startswith(os.path.join(proj_root, ign)):
                ignore_flag = True
                break

        if not ignore_flag:
            print('*', root)
            if root.endswith('__pycache__'):
                dirname = os.path.dirname(root)
                dst_dir = os.path.join(deploy, dirname.replace(proj_root, ''))
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                for file in files:
                    src = os.path.join(root, file)
                    new_file = str(file.split('.')[0]) + '.' + str(file.split('.')[-1])
                    dst = os.path.join(dst_dir, new_file)
                    shutil.copyfile(src, dst)
            else:
                dst_dir = os.path.join(deploy, root.replace(proj_root, ''))
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                for file in files:
                    if not file.endswith('.py'):
                        src = os.path.join(root, file)
                        dst = os.path.join(dst_dir, file)
                        shutil.copyfile(src, dst)


if __name__ == '__main__':
    proj_root = '../'
    deploy = '../../xio-intrusion-detection-deploy'
    build_deployment(proj_root, deploy, ['.git', '.idea'])
