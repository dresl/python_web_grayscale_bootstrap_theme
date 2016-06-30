#!bin/bash

if vagrant box update && vagrant up ; then
   echo "Succeeded"
else
   "Kernel will be recompiled"
   sudo /etc/init.d/vboxdrv setup
fi
