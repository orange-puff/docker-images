# docker-images

Run `build.py` to build the docker images in this repo

If the argument is `all`, this script will build every docker image. 

If the argument is not all, all arguments are assumed to be paths to docker files which the program will build

The directory structure is assumed to be:
```
dir0/dir1/.../dir{n-1}/dockerfile
dir0/dir1/.../dir{n-1}/version
```

the docker image name will be:
`dir0/dir1/.../dir{n-1}:version`