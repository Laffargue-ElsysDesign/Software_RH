# STM32CubeIDE project for Elsys-Design Holo Robot

This Directory include the complete Software used for the 2022 Holo project

# Hardware Configuration to program the board

![Alt text](../images/STM32_HW_Programming.jpg?raw=true "Programming Holo board")

Connect the ST Link to a USB Port of your PC

# How to use it

A litle guide if you want to debug it/ make changes and you are new to STM32CudeIDE. However, this Software should already be loaded to the STM32.

* Download and install STM32CudeIDE: https://www.st.com/en/development-tools/stm32cubeide.html
* Download and install STLink: I think I used this one but I maght be wrong here: https://www.st.com/en/development-tools/stsw-link004.html
* Clone the repo. We assume you will clone it to ~/Documents but you can replace the path by your own path if you cloned it somewhere else

```
git clone http://github.com/Laffargue-ElsysDesign/Software_RH.git
```

* Open STM32CubeIDE
* Choose ~/Documents/Software_RH/STM32 as your working directory
* Import Project From System File: ~/Documents/Software_RH/STM32/HoloSoft
* Check the Hardware Connection as seen before
* By pressing "Debug" you will be able to debug properly the program. Each time you press debug, the code is loaded. If you unplug the STLink and reboot the board (By turning it Off and then On), the last code loaded will run.


