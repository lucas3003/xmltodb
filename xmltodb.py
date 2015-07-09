import xml.etree.cElementTree as ET
import sys


#Parse variables of device and return list of dependent devices
def newDevice(device):
	global commands

	#Get index of the name
	for i in range(len(device)):
		if str(device[i].tag) == "name":
			nameIndex = i
			break	

	index = -1

	#Get index of... index
	for i in range(len(device)):
		if str(device[i].tag) == "index":
			index = i
			break

	if index == -1: #Index not found. Put 0 as default
		asynPort = device[nameIndex].text+"_0"
	else:
		asynPort = device[nameIndex].text+"_"+device[index].text

	dependentDevices = []

	records = ""

	ui = ""
	lastY = 0


	for child in device:
		if child.tag == 'variable':
			#records += parseVariable(child, asynPort)
			result = parseVariable(child,asynPort, lastY)
			records += result[0]
			ui += result[1]
			lastY += 30

		elif child.tag == 'device':
			dependentDevices.append(child)

		elif child.tag == 'command':
			commands += parseCommands(child, asynPort)


	# Create file with string 'records'
	#file = open("out/"+asynPort+".db", "w")
	file = open(sys.argv[2]+"/"+asynPort+".db", "w")
	file.write(records)
	file.close()


	ui_header = '<ui version="4.0"> \n <class>MainWindow </class> \n <widget class="QMainWindow" name="MainWindow"> \n <property name="geometry"> \n <rect> \n <x> 0 </x> \n <width> 442 </width> \n <height> %s </height> \n </rect> \n </property> \n <property name="windowTitle"> \n <string>MainWindow</string> \n </property> \n <widget class="QWidget" name="centralWidget"> \n' % (str(lastY + 30))
	ui_foot = '</widget> \n </widget> <customwidgets> \n <customwidget> \n <class>caMenu</class> \n <extends>QComboBox</extends> \n <header>caMenu</header> \n </customwidget> \n <customwidget> \n <class>caRelatedDisplay</class> \n <extends>QWidget</extends> \n <header>caRelatedDisplay</header> \n </customwidget> \n <customwidget> \n <class>caTextEntry</class> \n <extends>caLineEdit</extends> \n <header>caTextEntry</header> \n </customwidget> \n <customwidget> \n <class>caLineEdit</class> \n <extends>QLineEdit</extends> \n <header>caLineEdit</header> \n </customwidget> \n </customwidgets> \n <resources/> \n <connections/> \n </ui>'
	file = open(sys.argv[2]+"/"+asynPort+".ui", "w")
	file.write(ui_header + ui + ui_foot)
	file.close()

	return dependentDevices



def parseVariable(var, portName, lastY):
	enumVal = ["ZRVL", "ONVL", "TWVL", "THVL", "FRVL", "FVVL", "SXVL", "SVVL", "EIVL", "NIVL", "TEVL", "ELVL", "TVVL", "TTVL", "FTVL", "FFVL"]	
	enumStr = ["ZRST", "ONST", "TWST", "THST", "FRST", "FVST", "SXST", "SVST", "EIST", "NIST", "TEST", "ELST", "TVST", "TTST", "FTST", "FFST"] 
	enum = []

	name = ""
	desc = ""
	status = ""


	#Get information
	for child in var:

		if child.tag == 'name':
			name = child.text

		if child.tag == 'description':
			desc = child.text

		if child.tag == 'type':
			if child.text == 'Configuration':
				status = 0
			elif child.text == 'Status':
				status = 1

		if child.tag == 'enum':
			enum.append(child.text)

	#Create record

	new = ""
	new += "record("

	ui = ""
	ui += '<widget class="QLabel" name="%s">\n <property name="geometry"> \n <rect> \n <x> 50 </x> \n <y> %s </y> \n <width> 90 </width> \n <height> 15 </height> \n </rect> \n </property> <property name="text"> \n <string> %s </string> \n </property> \n </widget> \n' % (name, str(lastY+30), name)

	#Check type
	if status and len(enum) == 0:
		#new += "ai, "
		new += "stringin, "
		#dtyp = "asynFloat64"
		dtyp = "asynOctetRead"
		ui += '<widget class="caLineEdit" name="%s"> \n <property name="geometry"> \n <rect> \n <x> 140 </x> \n <y> %s </y> \n <width> 211 </width> \n <height> 20 </height> \n </rect> \n </property> \n <property name="channel" stdset="0"> \n <string notr="true"> %s </string> \n </property> \n </widget>' %  ("$(DEVICE):"+name, str(lastY+30), "$(DEVICE):"+name)
	elif not status and len(enum) == 0:
		#new += "ao, "
		new += "stringout, "
		#dtyp = "asynFloat64"
		dtyp = "asynOctetWrite"
		ui += '<widget class="caTextEntry" name="%s"> \n <property name="geometry"> \n <rect> \n <x> 140 </x> \n <y> %s </y> \n <width> 211 </width> \n <height> 20 </height> \n </rect> \n </property> \n <property name="channel" stdset="0"> \n <string notr="true"> %s </string> \n </property> \n </widget>' %  ("$(DEVICE):"+name, str(lastY+30), "$(DEVICE):"+name)
	elif status and len(enum) > 0:
		new += "mbbi, "
		dtyp = "asynInt32"
		ui += '<widget class="caLineEdit" name="%s"> \n <property name="geometry"> \n <rect> \n <x> 140 </x> \n <y> %s </y> \n <width> 211 </width> \n <height> 20 </height> \n </rect> \n </property> \n <property name="channel" stdset="0"> \n <string notr="true"> %s </string> \n </property> \n </widget>' %  ("$(DEVICE):"+name, str(lastY+30), "$(DEVICE):"+name)
	elif not status and len(enum) > 0:
		new += "mbbo, "
		dtyp = "asynInt32"
		ui += '<widget class="caMenu" name="%s"> \n <property name="geometry"> \n <rect> \n <x> 140 </x> \n <y> %s </y> \n <width> 211 </width> \n <height> 20 </height> \n </rect> \n </property> \n <property name="channel" stdset="0"> \n <string notr="true"> %s </string> \n </property> \n </widget>' %  ("$(DEVICE):"+name, str(lastY+30), "$(DEVICE):"+name)

	#Check name
	new += "$(DEVICE):"
	new += name + ")"
	new += "\n{\n"

	new+= 'field("DTYP", "'+dtyp+'")\n'

	#Check description
	if desc != "":
		new+= 'field("DESC", "'+desc+'")\n'

	#Check status
	if status:
		new+= 'field("INP", "@asyn('+portName+')'+name+'")\n'
	else:
		new+= 'field("OUT", "@asyn('+portName+')'+name+'")\n'
	
	
	new+= 'field("SCAN", "$(SCAN)")\n'

	if len(enum) > 0:
		i = 0

		for val in enum:
			new+= 'field("'+enumVal[i]+'", "'+str(i)+'")\n'		
			new+= 'field("'+enumStr[i]+'", "'+str(val)+'")\n'		
			i += 1

	new+= 'info(asyn:READBACK, "1")\n'

	new += "}\n\n"

	return [new, ui]

def parseCommands(command, asynPort):

	name = command[0].text
	desc = command[1].text

	hasArg = False

	for i in range(len(command)):
		if str(command[i].tag) == "hasArg":
			hasArg = True
			break

	new = ""
	new += 'record(bo, "$(DEVICE):'+name+'")\n{\n'
	new += 'field("DTYP", "asynInt32")\n'
	new += 'field("DESC", "'+desc+'")\n'
	new += 'field("OUT", "@asyn('+asynPort+')'+name+'")\n'
	new+= 'field("SCAN", "$(SCAN)")\n'
	new+= 'info(asyn:READBACK, "1")\n'
	new += "}\n\n"

	if hasArg:
		new += 'record(stringout, "$(DEVICE):'+name+'Arg")\n{\n'				
		new += 'field("DTYP", "asynOctetWrite")\n'
		new += 'field("DESC", "'+desc+'")\n'
		new += 'field("OUT", "@asyn('+asynPort+')'+name+'Arg")\n'
		new+= 'field("SCAN", "$(SCAN)")\n'
		new+= 'info(asyn:READBACK, "1")\n'
		new += "}\n\n"
			
	return new

def index(device):

	devices = newDevice(device)

	if len(devices) == 0:
		return

	for dev in devices:
		index(dev)


tree = ET.ElementTree(file=sys.argv[1])


commands = ""
system = tree.getroot()
structure = system[0]
index(structure)

file = open(sys.argv[2]+"/commands.db", "w")
file.write(commands)
file.close()