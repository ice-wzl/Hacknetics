## Linux Basics
### File Structure
- Linux uses the filesystem hierarchy standard which defines the way directories/folders are laid out. 
- It’s important to understand this structure to understand how the operating system works. 
- The top most directory is called the root directory(/). 
- Since the file system is organised in a hierarchy, every file and folder is located under the root directory. Here’s the most common layout of the root directory:
- `/bin` - contains programs in the form of binary files that user can run
- `/boot` - contains the files needed to start the system
- `/dev` - used to represent devices(mostly virtual) that correspond to particular functions
- `/etc` - contain configuration files for services on a computer and some system files
- `/usr` - contain executable files(programs) for most system programs
- `/home` - contains home directories for personal users
- `/lib` - contain libraries(which contain extra functions) that are used by executable files in the /bin directories
- `/var` - mostly contain files that store information about how services run(also known as log files)
- `/proc` - contains information about processes running on the system
- `/mnt` - used to mount file systems. Mounts are usually used when users want to access other file systems on their system
- `/opt` - contains optional software
- `/media` - contains removable hardware e.g. USB 
- `/tmp` - contains temporary files. This folder is usually cleared on reboot so doesn’t store persistent files
- `/root` - contains files created by the super user(more on this later)
### Password File
- The format of the file would be:
````
username[1]:x[2]:userid[3]:groupid[4]:useridinfo[5]:/folder/location[6]:/shell/location[7]
````
- [1] username
- [2] usually an x character and is used to represent their passwords
- [3] User ID
- [4] Group ID
- [5] Extra comments about a user
- [6] Home Directory
- [7] Shell Location - Most actual users will use the aforementioned shells, but accounts can also belong to particular services. 
- These services won’t have paths to shells but files like /sbin/nologin which means that the user can’t access this account through a shell(sometimes not at all)
- Another note to mention is that the /etc/passwd file is world readable. This is a useful file to display as a proof of concept to show that you have access to a system. A similar such file is the /etc/shadow file that actually contains password hashes of the user.









