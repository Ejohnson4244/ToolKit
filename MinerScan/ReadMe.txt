This script is a versitile scanning script that gathers several bits of miner data. including:
	1. IP address
	2. Possible Asset Tag (Pulled from Workername, may be inaccurate)
	3. Location (Pulled from Site Location sheet in /Locations/ foler)
	4. Hostname
	5. Workername
	6. Miner Type
	7. Control Board Type (If supported)
	8. Fan control (On = %/ Auto = Machine controlled)
	9. Fan %
	10. Workmode (Normal/ Sleep)
	11. Firmware Version (Date)

-Before running:
	- Ensure Run.bat file is updated according to your directory
	- Ensure all libraries/modules are installed
	- Ensure the (Possibly hidden) /Locations foler has an acurate list of YOUR site.

- Libraries needed for this script: requests, pandas
	- If you do not have these libraries installed, input the following commands into cmd prompt:
		1. curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		2. python get-pip.py
		3. pip install requests
		4. pip install pandas

- To run:
	- Export Minder list including an IP column. 
	- Drag miner.csv file(s) to the /CSV Files/ foler
	- Run the Run.bat file

- Script will
	- Read through "ip" column in /CSV Files/
	- Try all items in the pwd.txt file to log into machine
	- Query machine for all requested info and build a DataFrame
	- Export list info in ther DataFrame to a .csv, Renaming it "Scan_[Timestamp].csv"
	- Flag inconsistent hostname/workername info
	- Move the original list to the /Archive/ folder for record keeping. 	

- Notes
	- Some items are not supported to be pulled by certain model types
	- If Hostname and Workername do not include matching assets, Workername will be
		changes to "XX [workername] XX" as to flag incorrect host information
		- These are easily identifiable with filtering Workername header in csv for "XX"
	- This is created for S19s; however it should work on any Antminer machines, but not 
		other manufacturers. 
	-If you have any issues/ would like to request changes that may benefit your situation please 		reach out to me on slack or email.
		-Ethan Johnson
		-ejohnson@corescientific.com


















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