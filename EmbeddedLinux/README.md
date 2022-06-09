# PYNQ for Zybo-Z7-20 Repo

Final image can be found here: https://drive.google.com/file/d/1COR9SHoGHiNd57T-1oZzoWESZvyLyB8e/view?usp=sharing

## Environement requirements: 
Ubuntu Version tested: 18.04.4. Download it here : http://old-releases.ubuntu.com/releases/18.04.4/ubuntu-18.04-desktop-amd64.iso

If you are using VirtualBox, follow this guide to access your sdcard inside the virtual machine: https://scribles.net/accessing-sd-card-from-linux-virtualbox-guest-on-windows-host/

Setup your linux to passwordless when using sudo. This step is not necessary but the build will be easier because PYNQ needs to sudo quite frequently so it will ask for your passwd during the build process if not set to passwordless, meaning you have to stay close to your compuer during a build that can take a couple of hours

* open /etc/sudoers file
* add this line at the end of the file:
```
linuxconfig ALL=(ALL) NOPASSWD:ALL
```
* Save and exit /etc/sudoers

## Build Process:

### Setting-up PYNQ repository

```
git clone --recursive https://github.com/Xilinx/PYNQ.git
git clone https://github.com/Laffargue-ElsysDesign/Software_RH.git
```
Warning: We assume Software_RH and PYNQ folders are next to each other (in the same folder). If not you will have to modify command lines of this readme appropriately as well as the PYNQ_FOLDER macro in Software-RH/EmbeddedLinux/setup.sh file. You can change this macro to the absolute PATH of PYNQ folder
```
cd PYNQ/sdbuild/scripts
./setup-host.sh 
```
This may take some time
```
cd ../../../Software_RH
./setup.sh
```
Download Pynq rootfs arm 2.7 file in PYNQ/sdbuild folder: https://bit.ly/pynq_arm_2_7. Do NOT untar it.

### Setting-up xilinx tools

Warning Links for Downloads will ask you to register or create a Xilinx account + some personal information (Name, Country, Company). It is a requirement by Xilinx in order to Download their products.

For the next steps we assume your Download folder for Xilinx tools is ~/Download
* Download Xilinx Unified on the Download page of Xilinx website https://www.xilinx.com/member/forms/download/xef.html?filename=Xilinx_Unified_2020.2_1118_1232_Lin64.bin
* Download Petalinux Installer on Xilinx Website as well https://www.xilinx.com/member/forms/download/xef.html?filename=petalinux-v2020.2-final-installer.run
* Download patch y2k22 for vivado (Required since January 2022). End of this page: https://support.xilinx.com/s/article/76960?language=en_US
```
cd ~/Downloads
sudo -s
chmod +x Xilinx_Unified_2020.2_1118_1232_Lin64.bin
chmod +x petalinux-v2020.2-final-installer.run

mkdir -p /opt/pkg/Petalinux
mkdir -p /opt/pkg/Xilinx
chown username /opt/pkg
chgrp username /opt/pkg
chown username /opt/pkg/Petalinux
chgrp username /opt/pkg/Petalinux
chown username /opt/pkg/Xilinx
chgrp username /opt/pkg/Xilinx
exit

./petalinux-v2020.2-final-installer.run -d /opt/pkg/Petlainux
./Xilinx_Unified_2020.2_1118_1232_Lin64.bin
```
Of course when you select the install folder in the xilinx installer menu, choose /opt/pkg/Xilinx. Vivado Download will take time. Wait this process to end before continuing

Then you can source Xilinx and Petalinux settings scripts: 

* Open ~/.bashrc file
* add these lines at the end of the file:
```
source /opt/pkg/Petalinux/2020.2/settings.sh
source /opt/pkg/Xilinx/Vivado/2020.2/settings64.sh
source /opt/pkg/Xilinx/Vitis/2020.2/settings64.sh
```
* Save and exit .bashrc

### Vivado y2k22 Patch
```
unzip y2k22_patch-1.2.zip -d /opt/pkg/Xilinx
cd /opt/pkg/Xilinx
export LD_LIBRARY_PATH=$PWD/Vivado/2020.2/tps/lnx64/python-3.8.3/lib/
Vivado/2020.2/tps/lnx64/python-3.8.3/bin/python y2k22_patch/patch.py
```
* Close your current terminal and open a new one

### Build BSP

Go to PYNQ folder
```
petalinux-util --webtalk off
```
Open PYNQ/boards/Zybo-Z7/Zybo-Z7.spec file
Make sure it has the line BSP_Zybo-Z7 :=
```
cd sdbuild
make bsp BOARDS=Zybo-Z7
cp output//bsp/Zybo-Z7/xilinx-zyboz7-2020.2.bsp ../boards/Zybo-Z7/
```
Open PYNQ/boards/Zybo-Z7/Zybo-Z7.spec file
Add the bsp to the Zybo-Z7.spec: BSP_Zybo-Z7 := xilinx-zyboz7-2020.2.bsp.

### Build Image

Go back to PYNQ/sdbuild folder
```
make BOARDS=Zybo-Z7 PREBUILT=focal.arm.2.7.0_2021_11_17.tar.gz nocheck_images
```
Build will take a couple of hours. Image will be stored in output folder. Between 7.6 and 8.1 GB.
### Mount on SD card 
An 8GB sdcard might not be enough, 16 or 32 GB is better.
```
cd output
df -h
```
Select the device corresponding to your SD card. Be careful, you could damage your OS if choose wrong.
```
umount /dev/sXX1
```
(I had /dev/sdb1 and /dev/sdb2).
```
sudo dd bs=4M if=Zybo-Z7-2.7.0.img of=/dev/sXX status=progress
```
In my case : sudo dd bs=4M if=Zybo-Z7-2.7.0.img of=/dev/sdb status=progress

### Boot

* Connect your PC to Zybo J12 port with microUSB cable
* Connect J3 Ethernet of the Zybo to an internet source
* Plug the SDCard in the Zybo and set up to boot on sdcard
* Turn on the Zybo
* Open a Serial terminal : 
** baudrate 115200
** Data 8bits
** Parity None
** Stop bits 1
* Press PS-RST button to see boot process from the beginning 
* ifconfig and spot IP adress of your board
* Open a Browser (mozilla, chrome, brave, ...)
* Enter the IP adress
* Password xilinx
* Have fun

## Refrences used to achieve this work: 

### Environment Setup:
http://old-releases.ubuntu.com/releases/18.04.4/
https://www.virtualbox.org/
https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools.html
https://support.xilinx.com/s/article/76960?language=en_US

### PYNQ guide: 
https://pynq.readthedocs.io/en/latest/index.html
http://www.pynq.io/board.html

### Zybo-Z7 files: 
https://discuss.pynq.io/t/pynq-2-7-for-zybo-z7/4124
https://gitlab.com/dorfell/fer_sys_dev/-/tree/master/01_hw/Pynq_Zybo-Z7
