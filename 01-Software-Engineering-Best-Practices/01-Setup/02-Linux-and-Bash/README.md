# Linux Service creation

## Basics of services

🎯 The goal of this exercise is to create a background service on your virtual machine. Here we will write a script which checks whether you are connected via ssh and if not shutdown the vm in order to **prevent unwanted spending by leaving the vm running overnight!**

A service in linux is program that runs in the background outside of users which are not intended to be directly interacted with most of the time(sometimes they are also referred to as daemons).

🔎 Lets see which ones are currently on the virtual machine:

```bash
systemctl list-units --type=service
```

You'll get a huge list of services let reduce it to just the currently running ones!:

```bash
systemctl list-units --type=service | grep running
```

❗️ Two important bash motifs are shown in this command:

1️⃣ **The pipe `|`** which takes the standard output of one command and passes it as the input to the next one! This is easy to confuse with passing it as an argument but for example if we do 'echo 5 | echo' we get nothing as the standard input does not affect echo.

2️⃣ **[grep](https://www.gnu.org/software/grep/manual/grep.html)** which searches the input it receives for a pattern, in this example lines with `running` in them and returns only the lines matching the pattern.

From our command above and you will notice a couple of services that we are using already, the ssh.service is what is running in the background to allow ssh operate. **You'll also see two things we have installed docker and postgres which both run in background as services!**

If you had a lot more services and it was hard to see what was running you could also use `grep` to check whether postgres was there for example!

## Creating a script

❓ Start by creating a .sh script which checks whether any users are currently connected `echo` if there are and otherwise `poweroff`!

📚 Some things worth exploring in relation to the script if you are not familiar with bash scripts
- [why #!](https://www.linuxjournal.com/content/what-heck-hash-bang-thingy-my-bash-script)
- [control flow in bash](https://linuxcommand.org/lc3_wss0080.php)

<details>
<summary markdown='span'>Hint to check ssh users</summary>

```bash
ss | grep "tcp.*ssh"
```

</details>

<details>
<summary markdown='span'>Here is one way of writing a script if you get totally stuck</summary>

```bash
#!/bin/bash
connections=$(ss | grep "tcp.*ssh")
if [[ $connections ]]
then
    echo "Hey it looks like someone is connected"
else
    poweroff
fi
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

❗️ **The command we just used `chmod` can do more than just make a file executable**, it also affects who can read, write, and execute files! Here is a great [article](https://www.computerhope.com/unix/uchmod.htm) if you want to dig a bit more into this concept.

❓ Lets move our script into `/usr/local` before we move on, why do you think it is better to store it here?

## Creating a service

Next we need something to trigger our script, this is where services come in!

📚 This [article](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files) gives a great overview of how to create systemd units which are the building blocks we need to create our service.

❓ Start off by creating a `.service` file which triggers our script:

<details>
    <summary markdown='span'>Service example if you get stuck!</summary>

```bash
[Unit]
Description=test

[Service]
ExecStart=/bin/bash /usr/local/test.sh

[Install]
WantedBy=multi-user.target
```
</details>

## Creating a timer

Now we also need a .timer file to run our service which follows a similar syntax to services.

❓ We want to try and write a timer to trigger our service every 10 seconds:

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

❗️ **These files belong in the /etc/systemd/system directory**. The etc stands for editable text configuration, if you want a quick explanation of most of the folders in the root directory (i.e. the highest folder in the system) this explains the [linux filesystem](https://www.youtube.com/watch?v=42iQKuQodW4) well.

You might notice you get permission denied when trying to move the files into the folder you can fix this with sudo (a useful trick if you forget a sudo is running `sudo !!` runs the previous command but with sudo prepended).

You need this because the root user is the only user that can edit the root directory (along with everything on the system). Running `sudo` allows you to imitate this user to run one command (a more in-depth look at [root](http://www.linfo.org/root.html)). This control over absolutely everything on the system is one of the most powerful things about linux but you also must be careful not to overwrite key files as there is a lack of guard rails.

Now you can run `sudo systemctl daemon-reload` to make your service files available.

Run `sudo systemctl start <your_service>.service` to run the service once and check it does what you want it to. Then run `systemctl status test.service` to check if it is running! If you want more detailed logs you can use `sudo journalctl -r -u check_ssh`.

Next you want to use the timer here are the key commands from systemctl.
- `start` (starts the service/timer)
- `stop` (stops it)
- `enable` (always start on reboot but does not start now without --now)
- `disable` (stop it starting on reboot)

So to get our to run permanently we would use
```bash
sudo systemctl enable --now <your_service>.timer
```

In general though we don't want to run the service during the day after we have rebooted the vm, so lets use a different approach!

## Cron

Cron is an alternative way of running commands at a specific time of day, there are pros and cons to both but it is good to understand both. Cron is good for running short scripts at a particular time whereas services are much better for long running processes or process that have to be executed very often!

The syntax for cron is a little strange but to run `echo` once a day at 8pm you would write:

```bash
0 8 * * * echo 8
```

This [website](https://crontab.guru/#0_8_*_*_*) is great for checking your syntax!

Now we need to add this line but with echo replaced to start our timer and here is where we use crontab!

```bash
sudo crontab -e
```

This will open a file where you should write a line starting your service at a particular time! We need sudo here as our command we need to run is a command which requires root access but if you had something you wanted to run at a particular time for just your user you can just use `crontab -e`.

We now have a cron which starts a timer running on our to check if anyone is connected and if not shut it down, stopping us spending too much money by accidentally leaving it on overnight!
