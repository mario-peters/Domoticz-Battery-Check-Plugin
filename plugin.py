# Basic Python Plugin Example
#
# Author: GizMoCuz
#
"""
<plugin key="BatteryCheckPlugin" name="Battery Check Plugin" author="gizmocuz" version="1.0.0" wikilink="https://github.com/mario-peters/Domoticz-Battery-Check-Plugin/wiki" externallink="https://github.com/mario-peters/Domoticz-Battery-Check-Plugin">
    <description>
        <h2>Battery Check Plugin</h2><br/>
        Plugin to check the amount of voltage of battery-powered devices.
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>IP Address is the IP Address of the Domoticz server. Default value is 127.0.0.1</li>
            <li>Port Domoticz Server is the port on which Domoticz is running. Default value is 8084</li>
            <li>"# of checks a day" is the number of battery checks each day starting at 0:00. Possible values are:
                <ul style="list-style-type:square">
                    <li>1 (default value)</li>
                    <li>2</li>
                    <li>3</li>
                    <li>4</li>
                    <li>6</li>
                    <li>8</li>
                    <li>12</li>
                    <li>24</li>
                </ul>
            </li>
            <li>"Battery value threshold". If the battery value of a device is below this value, a notification will be send.</li>
            <li>"Notification system. Output mechanism which will be used. Possible values are:
                <ul style="list-style-type:square">
                    <li>email (default)</li>
                    <li>gcm</li>
                    <li>http</li>
                    <li>kodi</li>
                    <li>lms</li>
                    <li>nma</li>
                    <li>prowl</li>
                    <li>pushalot</li>
                    <li>pushbullet</li>
                    <li>pushover</li>
                    <li>pushsafer</li>
                </ul>
            </li>
        </ul>
        <br/><br/>
    </description>
    <params>
        <param field="Address" label="IP Address Domoticz server" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port Domoticz server" width="50px" required="true" default="8084"/>
        <param field="Mode1" label="# of checks a day" width="50px">
            <options>
                <option label="1" value="1" default="true"/>
                <option label="2" value="2"/>
                <option label="3" value="3"/>
                <option label="4" value="4"/>
                <option label="6" value="6"/>
                <option label="8" value="8"/>
                <option label="12" value="12"/>
                <option label="24" value="24"/>
            </options>
        </param>
        <param field="Mode2" label="Battery level threshold" width="50px" required="true" default="25"/>
        <param field="Mode3" label="Notification system" width="200px">
            <options>
                <option label="email" value="email" default="true"/>
                <option label="gmc" value="gmc"/>
                <option label="http" value="http"/>
                <option label="kodi" value="kodi"/>
                <option label="lms" value="lms"/>
                <option label="nma" value="nma"/>
                <option label="prowl" value="prowl"/>
                <option label="pushalot" value="pushalot"/>
                <option label="pushbullet" value="pushbullet"/>
                <option label="pushover" value="pushover"/>
                <option label="pushsafer" value="pushsafer"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import requests
import json
import datetime

class BasePlugin:
    enabled = False
    domoticzserver = "127.0.0.1"
    domoticzport = "8084"
    threshold = 25
    checksAday = 1
    hour = 0
    notification = ""
    
    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        Domoticz.Heartbeat(30)
        self.domoticzserver = Parameters["Address"]
        self.domoticzport = Parameters["Port"]
        self.checksAday = int(Parameters["Mode1"])
        self.threshold = int(Parameters["Mode2"])
        if self.threshold > 100 or self.threshold < 0:
            Domoticz.Error("Threshold size out of boundary error (0<threshold>100). Default value 25 is being used")
        self.notification = Parameters["Mode3"]

    def onStop(self):
        Domoticz.Log("onStop called")
        
    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called "+str(self.hour))
        
        if datetime.datetime.now().hour == self.hour:
            checkBatteryLevel(self)

            if self.checksAday == 1:
                if self.hour == 0 and datetime.datetime.now().hour == 0:
                    self.hour = 1
                else:
                    self.hour = 0

            if self.checksAday == 2:
                self.hour = self.hour + 12
            if self.checksAday == 3:
                self.hour = self.hour + 8
            if self.checksAday == 4:
                self.hour = self.hour + 6
            if self.checksAday == 6:
                self.hour = self.hour + 4
            if self.checksAday == 8:
                self.hour = self.hour + 3
            if self.checksAday == 12:
                self.hour = self.hour + 2
            if self.checksAday == 24:
                self.hour = self.hour + 1

            if self.hour == 24:
                self.hour = 0

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def checkBatteryLevel(self):
    headers = {'content-type':'application/json'}
    response_devices = requests.get("http://"+self.domoticzserver+":"+self.domoticzport+"/json.htm?type=devices&used=true&order=name",headers=headers)
    json_items = json.loads(response_devices.text)
    for key_item, value_item in json_items.items():
        Domoticz.Debug(key_item+" --> "+str(value_item))
        if key_item == "result":
            for device in value_item:
                Domoticz.Debug(str(device))
                batterylevel = 0
                name = ""
                for deviceparam_key, deviceparam_value in device.items():
                    if deviceparam_key == "BatteryLevel":
                        batterylevel = int(deviceparam_value)
                    if deviceparam_key == "Name":
                        name = deviceparam_value
                if batterylevel < self.threshold:
                    Domoticz.Log("Device ["+name+"] has batterylevel "+str(batterylevel))
                    body="Batterylevel of device "+name+" is below "+str(self.threshold)+"% ( "+str(batterylevel)+" )"
                    body=body.replace("%","%25")
                    body=body.replace(" ","%20")
                    body=body.replace("(","%28")
                    body=body.replace(")","%29")
                    response_notification=requests.get("http://"+self.domoticzserver+":"+self.domoticzport+"/json.htm?type=command&param=sendnotification&subject=Batterycheck&body="+body+"&subsystem="+self.notification,headers=headers)
