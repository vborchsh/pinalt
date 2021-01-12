# pinalt(ium)

Script for parsing files with pins description, exported from Altium

### Requirements

python3.xx

> Tested with 3.8, 3.9 (Win10, Linux, MacOS)

### Input .csv file
- Open Altium schematic (.PcbPrj file)
- Right click to intersted IC
- Pin mapping...
- Window with pins description will open
- Press "Export..." in the right down part of window
- Save file

### Running

Linux/MacOS

`python pinalt.py <csv file> <ignoring nets, separated by space>`

Windows

`python.exe pinalt.py <csv file> <ignoring nets, separated by space>`

> Example:
>
> `python pinalt.py example.csv GND +1,8V +1,2V +3,3V`

### Results:

В директории со скриптом создаются (перезаписываются без подтверждения) три файла:
There are three files:

<csv filename>net.txt - all nets list, sorted

<csv filename>.qsf - Intel Quartus pin description file

<csv filename>.xdc - Xilinx Vivado pin description file

! All those files will rewrited witohut any confirmations