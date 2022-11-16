# Docker under the hood

This exercise will try and take some of the magic away from containers and
guide you through creating a python script which creates your own fully isolated
ubuntu container!

TODO: Give more precise explanation of what we are going to do, in which order.

## Starting our project

This time, we don't want to give you a pre-defined virtual env in which to hook into poetry for reasons that will be demonstrated later!

❓ Let's create our own project from scratch:

```bash
poetry new <script_name> && cd $_
touch <script_name>/main.py
```
TODO: what script_name do you want us to create?
TODO: Where is the solution of the script? pyocker.py? Why not part of a packaged and called main.py in that case?

Now we have somewhere to install packages

## Getting ubuntu

To start our container off we are going to stick to ubuntu for simplicity but
we are going to hook into the [docker api](https://docs.docker.com/registry/spec/api/).
So that our containerization script could be generalized to run other docker images!

TODO: I don't understand this sentence - without more context on what we are trying to do, it makes little sense. Neither can't I understand anything from the docs, without context.

Here are some resources to get you started

- [Docker - auth explained](https://docs.docker.com/registry/spec/auth/token/)
- [Docker - Token api](https://auth.docker.io/token)
- [Docker - Registry api](https://registry-1.docker.io/v2/)
- [Requests - Docs](https://requests.readthedocs.io/en/latest/)
- [Subprocess - Docs](https://docs.python.org/3/library/subprocess.html)

Lets create a python function to extract ubuntu into a given directory
(although it might be easier to use the endpoints in postman initially)!

The pseudo code is as follows:

```markdown
1. Call token api and get a token
2. Get manifest for ubuntu from registry api
3. Get layer for ubuntu from registry api
4. extract into a given api
```
TODO: I have 0 idea what you are trying us to do here.

If you get stuck on any of the four parts the hints follow
<details>
<summary markdown='span'>Token api</summary>

```
https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/ubuntu:pull&client_id=ogiles1999
```
</details>

<details>
<summary markdown='span'>Manifest api</summary>

```
https://registry-1.docker.io/v2/library/ubuntu/manifests/latest
```
with a header including
```
Authorization: bearer <your_token>
```
</details>

<details>
<summary markdown='span'>Layer api</summary>

```
https://registry-1.docker.io/v2/library/ubuntu/blobs/<sha from manifest>
```
</details>

<details>
<summary markdown='span'>Extraction command</summary>

```bash
tar -xf <your_file.tar>
```
</details>

Now lets test your function create a file and add a block to the end of your
file to run the extraction

```bash
mkdir test_folder
```

```python
if __name__ == "__main__":
    extract_ubuntu("test_folder_path")
```

```bash
<script_name>/<script_name>.py
```

If your ubuntu function is working properly when you run `ls test_folder` you
should see the following:
![ubuntu folders](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D1/extracted-ubuntu.png)

You can also add a call to cleanup the `ubuntu.tar` but it is not necessary!

## Temporary directory

Now we have the files we need, lets also create somewhere to put those files. We don't want to have to manage creating and cleaning up lots of folders ourselves so lets use the inbuilt [tempfile](https://docs.python.org/3/library/tempfile.html) module!

Create a new run function which creates and cleans up temporary directory. Then inside this process call your previously created function to extract ubuntu files into the temporary directory.

<details>
<summary markdown='span'>If you get stuck</summary>

Use a context manager to deal with cleanup!
```python
import tempfile
import pathlib

def run():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = pathlib.Path(temp_dir)

        get_ubuntu(temp_dir_path)
```

</details>

## Creating our container

Now we have a folder with all of the files we need in order to run an isolated container:

There are a lot of layers of isolation that we would need in order to fully comply with the [oci standard](https://opencontainers.org/) but lets focus on the main ones:

- restricted memory without having a hypervisor completely sectioning off memory (like we would have on a virtual machine)
- isolated file system
- isolated processes (i.e. the container can't see the processes occurring on the rest of the machine!)
- fully functional (i.e. linux is fully functional within the bounds of the container!)

Lets do these step by step!

## Restricting memory

The way linux restricts memory is with [cgroups](https://man7.org/linux/man-pages/man7/cgroups.7.html) these deal with lots of the system and we would probably want to restrict all of them in some way but lets stick to just restricting our process to one cpu

First lets install [cgrouptools](https://reposcope.com/package/cgroup-tools) to help us

```bash
sudo apt-get cgroup-tools
```

Our first step is to create a new cgroup controlling cpu usage!

```bash
sudo cgcreate  -g cpu,cpuacct:/<group_name>
```

Now lets set a limit on the group here we are restricting the group to 256 shares this might see like an odd number. The default is 1024 so that means the default cgroup has 1024, therefore if process are running which would each use as much cpu as possible the original group would get 80% of cpu usage and our new cgroup 20%!

```bash
sudo cgset -r cpu.shares=256 <group_name>
```

Now lets run a process and check that is using the proper cgroup!

```bash
sudo cgexec -g cpu:/<group_name> /bin/bash
```

Lets find our process and check the cgroup, in a new terminal window run:

```bash
ps -aux
```

You should see all the processes and at at the bottom hopefully your `ps` and `/bin/bash`

![ps -aux](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D1/ps-aux.png)

The second column has our process id we need to check the cgroup is being used properly!

```bash
cat /proc/<your process id>/cgroups
```

You should see a print out of all the cgroups for that process and under `9:cpu,cpuacct:` you should see your group being used for this process (you can see all work we still would need to do to fully isolate everything)!

Now we have a command to prepend our final script with in order to make it run with a particular control group!

## Isolated file system

Next we need to work on isolating our file system here we are going to go with the 'naive' approach of using `chroot`!

We want to execute a few terminal commands on the startup of our container python does not necessarily have the best interface to run lots of command consecutively. Instead we can use it here to write a ".sh" script with the commands we need and copy that into our temporary directory!

Our `.py` file should take one argument which is the command to run inside the container. To start try and write a `.sh` that just, runs that argument. Then make the script executable and put it in our temporary directory.

<details>
<summary markdown='span'>If you get stuck</summary>

```bash
import sys

arg = sys.argv[1]

with open("startup.sh", "w") as f:
    f.writelines([
        "#!/bin/bash\n",
        arg
    ])
subprocess.run(["sudo", "chmod", "+x", "startup.sh"])
subprocess.run(["mv", "startup.sh", temp_dir])
```
</details>

Next we want to work on making the file root of our container's file system at our temporary directory. So
after we have setup everything ready to go we want to,
move into the directory and `chroot` running our terminal command! Something to note here is that you will need to run the script as root!

The behavior we hope to see is that when running our script with `pwd`, it should return `/`!

<details>
<summary markdown='span'>If you get stuck on chroot in python</summary>

```bash
os.chdir(temp_dir_path)
subprocess.run(["chroot", temp_dir, "./startup.sh"])
```

</details>

<details>
<summary markdown='span'>If you get stuck running the script as root</summary>

```bash
sudo $(poetry env info -p)/bin/python <your_script>.py pwd
```
</details>

Now if you run your script with `/bin/bash` instead you can explore your container! You can notice one issue here the hostname is still the same which might not be ideal.

Also try and run `ps` you'll get a command `mount -t proc proc /proc`. If you do this and run `ps -aux` it will now work but you can also see all the processes on the rest of your machine so we need to remove that!

Before we remove the view on the other processes lets add two more lines to our startup script

```bash
hostname <a name>
mount -t proc proc
```

## Isolating the process

The final step we are going to cover is about isolating the process from the rest of the processes on the system here we just need to use the [unshare](https://man7.org/linux/man-pages/man1/unshare.1.html) command to unshare the the PID namespace!

Lets just unshare the `pid`, `user`, and mount to make it as simple as possible (still quite difficult)!

<details>
<summary markdown='span'>If you get stuck!</summary>

```bash
unshare -mpfu chroot
```

</details>

Now if you enter the container and run `ps -aux` process 1 should be our startup script!!!

## Putting it all together

We can now run:

```bash
sudo cgexec -g cpu:/<group_name> <path to python env> <your_script> <args>
```

Giving us a container running with our created cgroup, with a new file system, and isolated PID!

## Still to do

This is a pretty great level of isolation especially for one exercise but there are a few things still to do if we wanted to take it further

- Make a command to run our now quite long and ugly command!
- Networking for the container
- Isolation of all the groups
- Fully setup the cgroup
- chroot is slightly `naive` and you can break out of it (you can instead use a more advanced tool like [firejail](https://firejail.wordpress.com/))
- Setup a union file system ([readmore here](https://martinheinz.dev/blog/44)) at the moment each container takes up the space of the ubuntu.tar on memory!
