# Linux Service creation

## Basics of services
The goal of this exercise is to create a background service on your virtual machine. Here we will write a script which checks whether you are connected via ssh and if not shutdown the vm in order to prevent unwanted spending by leaving the vm running overnight!

A service in linux is program that runs in the background outside of users which are not intended to be directly interacted with (sometimes called daemons).

Lets see which ones are currently on the virtual machine:

```bash
systemctl list-units --type=service
```

You'll get a huge list of services let reduce it to just the currently running ones:

```bash
systemctl list-units --type=service | grep running
```

You'll notice a couple of services that we are using already, the ssh.service is what is running in the background to allow ssh operate. You'll also two things we have installed docker and postgres which both run in background as services!

### Creating a script

Start by creating a .sh script which checks whether any users are currently connected `echo` if they are and if there are not any `poweroff`!

Some things worth exploring in relation to the script
- [why #!](https://www.linuxjournal.com/content/what-heck-hash-bang-thingy-my-bash-script)
- [control flow in bash](https://linuxcommand.org/lc3_wss0080.php)

<details>
<summary markdown='span'>Hint to check ssh users</summary>

```bash
ss | grep "tcp.*ssh"
```
</details>

Once you have your .sh script you need to make it executable, this is the fastest way:

```bash
chmod +x <your_file.sh>
```
and now if you run it
```bash
./<your_file.sh>
```
You should see that someone is connected.

The command we just used `chmod` can do more than just make executable it also affects who can read, write, and execute files! Here is a great [article](https://www.computerhope.com/unix/uchmod.htm) if you want to dig a bit more into this concept.

## Creating a service

This [article](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files) gives a great overview of how to create systemd units which are the building blocks we need to create our service.

Start off by creating a .service files:

<details>
    <summary markdown='span'>Service example if you get stuck!</summary>

```bash
[Unit]
Description=test job

[Service]
Type=oneshot
ExecStart=echo 1
```
</details>

Now we also need a .timer file to run our service:

<details>
    <summary markdown='span'>Timer example if you get stuck!</summary>

```bash
[Unit]
Description=test

[Timer]
OnUnitActiveSec=10s
OnBootSec=10s

[Install]
WantedBy=timers.target
```
</details>

## Putting it all together

These files belong in the /etc/systemd/system directory. The etc stands for editable text configuration, if you want a quick explanation of most of the folders in the root directory (i.e. the highest folder in the system) this explains the [linux filesystem](https://www.youtube.com/watch?v=42iQKuQodW4) well.

You might notice you get permission denied when trying to move the files into the folder you can fix this with sudo (a useful trick if you forget a sudo is running `sudo !!` runs the previous command but with sudo prepended).

You need this because the root user is the only user that can edit the root directory (along with everything on the system). Running `sudo` allows you to imitate this user to run one command (a more in-depth look at [root](http://www.linfo.org/root.html)). This control over absolutely everything on the system is one of the most powerful things about linux but you also must be careful not to overwrite key files as there is a lack of guard rails.

Now you can run `sudo systemctl daemon-reload` to make your service files available.

Run `sudo systemctl start <your_service>.service` to run the service once and check it does what you want it to. Then run `systemctl status test.service` to check the logs!

Next you want to use the timer here are the key commands from systemctl.
- `start` (starts the service/timer)
- `stop` (stops it)
- `enable` (always start on reboot but does not start now without --now)
- `disable` (stop it starting on reboot)

So to get our service to work we want to run
```bash
sudo systemctl enable --now <your_service>.timer
```

We now have a service running on our vm!
