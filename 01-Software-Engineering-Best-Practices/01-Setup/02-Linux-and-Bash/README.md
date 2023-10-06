# 1️. Basics of services

🎯 The goal of this exercise is to create a **background service** on your virtual machine. Here we will write a script which checks whether you are connected via ssh and if not shutdown the vm in order to **prevent unwanted spending by leaving the vm running overnight!**

A **service** in linux is a program that runs in the background outside of users which are not intended to be directly interacted with most of the time (sometimes they are also referred to as **Daemons**).

🔎 Lets see which ones are currently on the virtual machine:

```bash
systemctl list-units --type=service
```

You'll get a huge list of services let reduce it to just the currently running ones!:

```bash
systemctl list-units --type=service | grep running
```

❗️ Two important bash motifs are shown in this command:

**The pipe `|`** which takes the standard output of one command and passes it as the input to the next one!
This is easy to confuse with passing it as an argument but for example if we do
```
echo 5 | echo
```
we get nothing as the standard input does not affect echo.

**[grep](https://www.gnu.org/software/grep/manual/grep.html)** which searches the input it receives for a pattern, in this example lines with `running` in them and returns only the lines matching the pattern.

From our command above and you will notice a couple of services that we are using already, the ssh.service is what is running in the background to allow ssh operate. **You'll also see two things we have installed docker and postgres which both run in background as services!**

If you had a lot more services and it was hard to see what was running you could also use `grep` to check whether postgres was there for example!

# 2️. Creating a script

❓ Let's start by creating a `check_ssh.sh` script which checks whether any users are currently connected, `echo` if there are and otherwise `poweroff` the VM!

📚 Some things worth exploring in relation to the script if you are not familiar with bash scripts
- Start by `#!/bin/bash` to tell your computer that this file should be run by `bash`
- Go back to the lecture and check the control flow syntax there!
- Use `ss | grep "tcp.*ssh"` to check for SSH users

<details>
<summary markdown='span'>Solution</summary>

```bash
#!/bin/bash
connections=$(ss | grep "tcp.*ssh" | wc -l)
if [[ $connections > 0 ]]
then
    echo "Hey it looks like someone is connected"
else
    poweroff
fi
```
</details>

❓ Let's now make `check_ssh.sh` executable (`x`):

```bash
chmod +x check_ssh.sh
```
and now if you run it:
```bash
./check_ssh.sh
```

You should see that someone is connected.

❗️ **The command we just used `chmod` can do more than just make a file executable**, it also affects who can read, write, and execute files! Bookmark this [great article](https://www.computerhope.com/unix/uchmod.htm) for later if you want to dig a bit more into this concept.
<img src='https://cdn.thegeekdiary.com/wp-content/uploads/2017/11/Files-permissions-and-ownership-basics-in-Linux.png' width=300>

❓ Lets move our script into `/usr/local` before we move on.

You might notice you get permission denied when trying to move the files into the folder you can fix this with sudo (💡 a useful trick if you forget a sudo is running `sudo !!` runs the previous command but with sudo prepended).You need this because the root user is the only user that can edit the root directory (along with everything on the system). Running `sudo` allows you to imitate this user to run one command (a more in-depth look at [root](http://www.linfo.org/root.html)). This control over absolutely everything on the system is one of the most powerful things about linux but you also must be careful not to overwrite key files as there is a lack of guard rails.

<details>
  <summary markdown='span'>💡 Why do /usr/local ?</summary>

If you want a quick explanation of most of the folders in the root directory (i.e. the highest folder in the system) this 2 min video explains the [linux filesystem](https://www.youtube.com/watch?v=42iQKuQodW4) at a high level.

</details>


# 3️. Creating a service

Next we need something to trigger our script, this is where **services** come in!

❓ Start off by creating a `check_ssh.service` file which triggers our script:

<details>
    <summary markdown='span'>💡 Service example</summary>

```bash
[Unit]
Description=some description

[Service]
ExecStart=/bin/bash /usr/local/test.sh

[Install]
WantedBy=multi-user.target
```
</details>

# 4️. Creating a timer

❓ Now create a `check_ssh.timer` file to trigger our service every 10 seconds

<details>
    <summary markdown='span'>💡 Timer example</summary>

```bash
[Unit]
Description=some description

[Timer]
OnUnitActiveSec=10s
OnBootSec=10s

[Install]
WantedBy=timers.target
```
</details>

# 5️. Running the service

❗️ **Move these `check_ssh.service` and `check_ssh.timer` in the `/etc/systemd/system` directory**.

Now you can run `sudo systemctl daemon-reload` to make your service files available.

Run `sudo systemctl start <your_service>.service` to run the service once and check it does what you want it to. Then run `systemctl status <your_service>.service` to check if it is running! If you want more detailed logs you can use `sudo journalctl -r -u check_ssh` to see every output.

Next you want to use the timer **here are the key commands from systemctl.**
- `start` (starts the service/timer)
- `stop` (stops it)
- `enable` (always start on reboot but does not start now without --now)
- `disable` (stop it starting on reboot)

So to get our to run permanently we would use
```bash
sudo systemctl enable --now <your_service>.timer
```

In general though we don't want to run the service during the day after we have rebooted the vm as we can be presumed to be using it then, so lets use a different approach! Disable the service and move on to next section.

# 6️. Cron

Cron is an alternative way of running commands at a **specific time** of day, there are pros and cons to both but it is good to understand both. Cron is good for running short scripts at a particular time whereas services are much better for long running processes or process that have to be executed very often!

Let's open the crontab that keep track of cron jobs

```bash
sudo crontab -e
```
❓ This will open a file where you should write a line starting your service at a particular time! Now you need to add a line to start our `check_ssh.timer`!

The syntax for cron is a little strange but for instance, to run `echo` once a day at 8pm you would write:

```bash
0 20 * * * echo "I'm going to be printed every day at 8pm"
```

This [website](https://crontab.guru/#0_20_*_*_*) is great for checking your syntax!

<details>
  <summary markdown='span'>💡 crontab solution</summary>

```bash
0 20 * * * systemctl start check_ssh.timer
````

</details>
Services and cron are two powerful tools in the linux arsenal, here we could have achieved our goal with either on their own but it is useful to know both in case only one is appropriate!

🏁 We now have a cron which starts a timer running on our to check if anyone is connected and if not shut it down, stopping us spending too much money by accidentally leaving it on overnight!
