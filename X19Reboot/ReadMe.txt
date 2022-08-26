This script is used to efficiently reboot Antminer units, made for S19s, but should work on any Antminer units. All active miner passwords are stored in the pwd.txt file (scripts cycles through this to find the match for the machine). Make sure the 
Minder view used for exporting has the IP column active.

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
- Drag downloaded minder.csv file(s) to the ./CSV Files/ folder
- Run the Run.bat file


Script will
- read through the "ip" column in the csv files
- try all items in pwd.txt to log into the machine
- Send a reboot signal to the IP address
- Move files in ./CSV Files/ folder to ./Archives/ folder
- Rename csv to "Reboot [timestamp].csv"






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