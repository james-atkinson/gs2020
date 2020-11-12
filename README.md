# Ground Services 2020
A ground services addon for Microsoft Flight Simulator 2020

### Features
* Jetway interaction
* Ability to call a fuel truck
* Manual pushback control
* Automated pushback (distance, turn direction, and angle of turn implemented) with automated parking brake option

### Planned Features
* Doors page to open/close aircraft doors
* Rudder pedal based pushback steering
* More pushback planning options including the ability to save/load pushback plans
* More ground services options if/when Asobo add them to the SDK
* Optional audio feedback from ground services

# Installation
Ground Services 2020 is a 2 part application, however only the GS2020 server is required to be installed. You can optionally also install an in-game panel that will allow you to access GS2020 from within the simulator itself. 

### Server Installation (required)
* Unzip the release package
* Copy the GS2020 folder to where you like to keep your addons. **DO NOT** put this folder into your community folder!.

### In Game Panel Installation (optional)
* Unzip the release package
* Copy the **fs-base-ingamepanels-gs** folder to the MSFS Community folder, locations vary:
  * For the Microsoft Store edition AND/OR Gamepass edition: `C:\Users\[YOUR USERNAME]\AppData\Local\Packages\Microsoft.FlightSimulator_<RANDOMLETTERS>\LocalCache\Packages\Community`.
  * For the Steam edition: `C:\Users\[YOUR USERNAME]\AppData\Roaming\Microsoft Flight Simulator\Packages\Community`.
  * For the Boxed edition: `C:\Users\[YOUR USERNAME]\AppData\Local\MSFSPackages\Community`.
  * If none of those locations work you can find you community folder by going into MSFS 2020 by doing the following:
    * Open general options and enabling developer mode. 
    * In the bar at the top of the screen find the tools menu, then virtual file system.
    * Click on watched bases, your community folder will be listed here.

# Usage
**IMPORTANT:** If you plan to use the in-game panel you **MUST** start GS2020 server **BEFORE** you start a new flight in MSFS 2020, the in-game panel will not work if the server is started after the flight.
Usage is simple, open your GS2020 folder and run **gs2020-server.exe**. This will open a terminal window and display some debugging text. You can minimize this window.

### Without the in-game panel
Open a browser (Chrome, Edge, Firefox etc.) and navigate to: (http://localhost:5000)

### With in-game panel
Start a flight and move your mouse to the bar at the top of the screen (the one that has ATC, VFR map etc.).
If you don't see a **GS20202** icon click on settings and enable Ground Services 2020
Open the **GS2020** panel and enjoy!

# Contributing
GS2020 is an open source application, if you wish to contibute to its development fork the repository at (https://github.com/james-atkinson/gs2020), make your changes, and submit a pull request.

# License
GNU GENERAL PUBLIC LICENSE Version 3


