# Ground Services 2020
A ground services addon for Microsoft Flight Simulator 2020

# Installation
Ground Services is a 2 part application, however only the GS2020 server is required to be installed. You can optionally also install an in-game panel that will allow you to access GS2020 from within MSFS 2020 itself. 

## In Game Panel Installation
* Unzip the release package
* Copy the **fs-base-ingamepanels-gs** folder to the MSFS Community folder, locations vary:

For the Microsoft Store edition AND/OR Gamepass edition:
`C:\Users\[YOUR USERNAME]\AppData\Local\Packages\Microsoft.FlightSimulator_<RANDOMLETTERS>\LocalCache\Packages\Community`.

For the Steam edition:
`C:\Users\[YOUR USERNAME]\AppData\Roaming\Microsoft Flight Simulator\Packages\Community`.

For the Boxed edition:
`C:\Users\[YOUR USERNAME]\AppData\Local\MSFSPackages\Community`.

If none of those locations work you can find you community folder by going into MSFS 2020 by doing the following:
* Open general options and enabling developer mode. 
* In the bar at the top of the screen find the tools menu, then virtual file system.
* Click on watched bases, your community folder will be listed here.

## Server Installation
* Unzip the release package
* Copy the GS2020 folder to whever you keep your addons. It **DOES NOT** have to be in the MSFS community folder. 

# Usage
Usage is simple, open your GS2020 folder and run **gs2020_server.exe**. It will open a terminal window and display some debugging text. You can minimize this window.

**IMPORTANT:** If you plane to use the in-game panel you MUST start GS2020 server **BEFORE** you start a new flight in MSFS 2020, the in-game panel will not work if the server is started after the sim.

If you are not using the in-game panel open a browser window an navigate to (http://localhost:5000)

Follow the instructions on the screen.

Enjoy!

# Contributing
GS2020 is an open source application, if you wish to contibute to it's development fork the repository at (https://github.com/james-atkinson/gs2020), make your changes, and submit a pull request.

# License
 GNU GENERAL PUBLIC LICENSE Version 3


