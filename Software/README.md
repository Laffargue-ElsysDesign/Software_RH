#Software

The folder is the actual program running in the robot, as detailed in the report (../RapportStage)

##To run this program: 

* Mount an SDCard with the PYNQ built in ../EmbeddedLinux
* Insert it in the Zybo-Z7-20 board
* Turn on the board with the correct configuration to boot on SDCard
* Inside the board you can run the following command
```
git clone http://github.com/Laffargue-ElsysDesign/Software_RH.git
cd Software_RH/Software/Brain
```
* You will normally the init file. you can run it :
```
python __init__.py
```
* The program will run. pass from manual to auto by pressing m, then enter.
