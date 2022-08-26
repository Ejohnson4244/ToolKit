This script is used for putting units into sleep mode, waking machines up, and changing fan speed configurations.
On running, you will be prompted with 3 config options to choose from. If sleep mode is chosen, it will copy the file 
to the "/Active Sleeping/" folder as to keep the list of units awaiting wake separate from the archive. 
Every list submitted to this script will be renamed following the format of "[operation] + [timestamp].csv" and 
moved to the "/Archive/" folder to keep records of when and which operations are completed.

- You will need to update the Windows Batch file to cd to directory containing the script
	- Right click on .bat file
	- Click "Edit"

- Libraries needed for this script: requests, pandas
	- If you do not have these libraries installed, input the following commands into cmd prompt:
		1. curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		2. python get-pip.py
		3. pip install requests
		4. pip install pandas


- Gather list in Minder (including an IP column)
- Drag downloaded miner.csv file(s) to the ./CSV Files/ folder
- Run the Run.bat file


Script will
- read through the "ip" column in the csv files
- try all items in pwd.txt to log into the machine
- Send the set config signal to the IP address
- Move files in ./CSV Files/ folder to ./Archives/ folder
- Copies list to ./Active Sleeping/ folder if the sleep config is chosen.

MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMN0OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO0XWMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMWKl'.........................................;kNMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMW0c............................................'dNMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMWO:..............................................'oXMMMMMMMMMMMMM
MMMMMMMMMMMMMMNk;.................................................lKMMMMMMMMMMMM
MMMMMMMMMMMMMNx,...................................................c0WMMMMMMMMMM
MMMMMMMMMMMMXd'.....................................................:0WMMMMMMMMM
MMMMMMMMMMMXl................'''''''''''''''''''''''''...............;kWMMMMMMMM
MMMMMMMMMWKc...............:OKKKKKKKKKKKKKKKKKKKKKKKKKd,..............,xNMMMMMMM
MMMMMMMMW0:...............lKMMMMMMMMMMMMMMMMMMMMMMMMMMNk;..............'dXMMMMMM
MMMMMMMWO;..............'oXMMMMMMMMMMMMMMMMMMMMMMMMMMMMWO:...............oXWMMMM
MMMMMMNk,..............'xNMMMMMWX0OOOOOOOOOOOOOO0KNMMMMMW0c...............lKWMMM
MMMMMNd'..............,kNMMMMMW0c'',,,,,,,,,,,,,,;dNMMMMMWKl...............:0WMM
MMMMXo...............;OWMMMMMWO;..................,oXWMMMMMXo...............;OWM
MMWKl...............:0WMMMMMNk,....................'lKWMMMMMNd'..............,kN
MW0c...............cKWMMMMMNd,......................'c0WMMMMMNx,..............,x
WO;...............oXMMMMMWXo'........................':OWMMMMMWKOkkkkkkkkkkkkkk0
k,..............'dXMMMMMWKl...........................':kNMMMMMMMMMMMMMMMMMMMMMM
,...............oXMMMMMMXo..............................;OMMMMMMMMMMMMMMMMMMMMMM
o...............;OWMMMMMWO;.............................lXMMMMMMMMMMMMMMMMMMMMMM
Nd'..............,kWMMMMMW0:..........................'oXMMMMMMNXXXXXXXXXXXXXXXN
MNx,..............'xNMMMMMWKc........................'xNMMMMMW0l,,,,,,,,,,,,,,:x
MMWk;...............oXMMMMMWXl'.....................,kWMMMMMWO;...............oX
MMMW0:...............lKWMMMMMXd'...................;OWMMMMMWk,..............'dXM
MMMMWKc...............c0WMMMMMNx,.................:0WMMMMMNx'..............,xNMM
MMMMMMXo...............:OWMMMMMN0xdddddddddddddddxKMMMMMMXd'..............;kNMMM
MMMMMMMXd'..............;kWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMXo...............:OWMMMM
MMMMMMMMNx'..............,xNMMMMMMMMMMMMMMMMMMMMMMMMMMWKc...............c0WMMMMM
MMMMMMMMMWk,..............'dXMMMMMMMMMMMMMMMMMMMMMMMMW0:...............lKWMMMMMM
MMMMMMMMMMWO;...............;cccllllllllllllllllclcclc,...............oXMMMMMMMM
MMMMMMMMMMMW0c......................................................'dNMMMMMMMMM
MMMMMMMMMMMMWKl....................................................,kNMMMMMMMMMM
MMMMMMMMMMMMMMXo..................................................;OWMMMMMMMMMMM
MMMMMMMMMMMMMMMNx'...............................................:0WMMMMMMMMMMMM
MMMMMMMMMMMMMMMMNk,.............................................lKWMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMWO;...........................................oXMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMWKdoooooooooooooooooooooooooooooooooooooooookNMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM