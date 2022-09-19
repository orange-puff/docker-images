import os
import sys
import subprocess

DOCKER_IMAGE_REPO = 'orangepuff'
global username
global password

"""
if the argument is 'all', this script will build every docker image. if the argument is not all,
all arguments are assumed to be paths to docker file directories which the program will build
directory structure is assumed to be 
dir0/dir1/.../dir{n-1}/dockerfile
dir0/dir1/.../dir{n-1}/version

the docker image name will be 
dir0/dir1/.../dir{n-1}:version
"""
def get_docker_file_directories():
    dirs = []
    q = [os.getcwd()]
    q_ind = 0

    while q_ind < len(q):
        curr_path = q[q_ind]
        q_ind += 1

        for path in os.listdir(curr_path):
            potential = os.path.join(curr_path, path)
            if os.path.isdir(potential):
                q.append(potential)
            elif path == 'dockerfile':
                dirs.append(curr_path)

    return dirs

def filter_directories(dirs):
    to_ret = []
    for dir in dirs:
        if os.path.isfile(os.path.join(dir, 'dockerfile')) and os.path.isfile(os.path.join(dir, 'version')):
            to_ret.append(dir)
    return to_ret

def build_docker_images(dirs):
    sub_path = os.getcwd()
    for dir in dirs:
        image_name = dir[len(sub_path) + 1:]
        print('building docker image for `' + image_name + '` ...')
        os.chdir(dir)

        # build the docker image
        args = ['docker', 'build', '-t', image_name, '.']
        print_command(args)
        subprocess.call(args)

        # get version
        version = None
        with open(os.path.join(dir, 'version')) as f:
            version = f.read().strip()

        # tag the docker image
        image_full_name = '{}/{}:{}'.format(DOCKER_IMAGE_REPO, image_name, version)
        args = ['docker', 'tag', image_name, image_full_name]
        print_command(args)
        subprocess.call(args)

        # loging to docker hub
        global username
        global password
        args = ['docker', 'login', '-u', username, '-p', password]
        print('running docker login')
        subprocess.call(args)

        # push the docker image
        args = ['docker', 'push', image_full_name]
        print_command(args)
        subprocess.call(args)

def print_command(args):
    print('\nrunning `{}`\n'.format(' '.join(args)))

def main():
    n = len(sys.argv)
    if n == 1:
        print('nothing to do...')
        return
    dirs = sys.argv[1:]
    if len(dirs) == 1 and dirs[0].lower() == 'all':
        dirs = get_docker_file_directories()
    else:
        cwd = os.getcwd()
        dirs = [os.path.join(cwd, dir) for dir in dirs]

    dirs = filter_directories(dirs)
    build_docker_images(dirs)

if __name__=='__main__':
    global username
    username = os.environ['DOCKER_USERNAME']
    global password
    password = os.environ['DOCKER_PASSWORD']
    main()
    