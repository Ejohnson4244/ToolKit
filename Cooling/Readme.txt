This script is used to cool off machines/ sections of units by stopping the machine from hashing (sleep mode) and 
changing the fan speeds to 100% for X amount of seconds. You can also alter the outcome configurations on the machine(s) 
by changing info in "payload2" inside the SleepMode.py file, parameters are given next to the values inside the .py. 
This script will stay open until all operations are completed, i.g., if you put units into sleep for 300 seconds, it will stay 
open for 300 seconds. Do not close the window early; the machines will not automatically come out of sleep mode if done so. 


- You will need to update the Windows Batch file to cd to your directory containing the script
	- Right click on .bat file
	- Click "Edit"
-Libraries needed for this script: requests, pandas
	- If you do not have these libraries installed, input the following commands into cmd prompt:
		1. curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		2. python get-pip.py
		3. pip install requests
		4. pip install pandas

- Gather list in Minder (including an IP column)
- Drag downloaded minder.csv file(s) to the ./CSV Files/ folder
- Run the Run.bat file


Script will
- read through the "ip" column in the csv files
- try all items in pwd.txt to log into the machine
- ask how long you would like the machines to sleep for, this argument is in seconds (1 min = 60, 5 min = 300, 8 min = 480, etc.)
- send a signal to the IP address that moves machine to sleep mode and moves fan speed to 100%(sleep fan speed is adjustable via payload1).
- wake up machines after sleep timer is done and restores fan speed to settings before sleep (fan speed is adjustable via payload2).
- move files in ./CSV Files/ folder to ./Archives/ folder
- Rename csv to "Cooling [timestamp].csv"

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