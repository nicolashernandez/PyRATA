The current environment allows to use the PyRATA API and run ``pyrata_re.py``. No GUI would be available currently to visualize pdf.

install docker
--------------
# do it once
::

    sudo apt-get install docker.io

# get an official ubuntu image
# images hub https://hub.docker.com
::

    sudo docker pull ubuntu


build a pyrata image 
--------------------
# do it once (except if you change the config file)

# remove existing built images  (if some have already been built)
::

    sudo docker ps -a -q | xargs -n 1 -I {} sudo docker rm {} && sudo docker rmi pyrataimage 

# list the images and get some informations
::

    sudo docker ps
    sudo docker images


# the config file is Dockerfile (this is the important part)
::

    cd PyRATADocker/
    sudo docker build -t pyrataimage . 

run the pyrata image 
----------------------

# do it when you want to run the image
# this open a term in the pyrataimage as root
# CTR+D to quit
::

    sudo docker run -i -t pyrataimage /bin/bash
    cd /root


