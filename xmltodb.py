#Lucas Jose Monteiro Carvalho
#SLAC National Accelerator Laboratory

import xml.etree.cElementTree as ET
import sys

def findIndex(device):
	index = -1

	#Get index of... index
	for i in range(len(device)):
		if str(device[i].tag) == "index":
			index = i
			break

	return index

def findNameIndex(device):
	#Get index of the name
	for i in range(len(device)):
		if str(device[i].tag) == "name":
			nameIndex = i
			break

	return nameIndex			


#Parse variables of device and return list of dependent devices
def newDevice(device):
	global commands

	nameIndex = findNameIndex(device)
	index = findIndex(device)

	if index == -1: #Index not found. Put 0 as default
		asynPort = device[nameIndex].text+"_0"
	else:
		asynPort = device[nameIndex].text+"_"+device[index].text

	dependentDevices = []

	records = ""

	ui = ""
	lastY = 30

	status_ui = []
	config_ui = []


	biggest_label_width = 0

	for child in device:
		if child.tag == 'variable':
			#result = parseVariable(child,asynPort, lastY)
			result = parseVariable(child, asynPort)
			records += result[0]
			ui = result[1]
			label_width = result[2]

			if label_width > biggest_label_width:
				biggest_label_width = label_width

			if 'caLineEdit' in ui:
				status_ui.append(result[1])
			else: #Configuration variable
				config_ui.append(result[1])	

		elif child.tag == 'device':
			dependentDevices.append(child)

		elif child.tag == 'command':
			commands += parseCommands(child, asynPort)


	if len(status_ui) > 0:
		status_label = '<widget class="QLabel" name="status">\n <property name="geometry"> \n <rect> \n <x> 50 </x> \n <y> %s </y> \n <width> 200 </width> \n <height> 15 </height> \n </rect> \n </property> <property name="text"> \n <string> %s </string> \n </property> \n </widget> \n' % (str(lastY), 'Status variables')
	
		lastY += 30


		status_ui_modified = []
		for s in status_ui:
			#print "status_ui for"
			temp = s.replace("YNOTDEFINED", str(lastY))
			temp = temp.replace("XNOTDEFINED", str(biggest_label_width+50))
			status_ui_modified.append(temp)
			lastY += 30

		lastY += 70

	if len(config_ui) > 0:
		config_label = '<widget class="QLabel" name="status">\n <property name="geometry"> \n <rect> \n <x> 50 </x> \n <y> %s </y> \n <width> 200 </width> \n <height> 15 </height> \n </rect> \n </property> <property name="text"> \n <string> %s </string> \n </property> \n </widget> \n' % (str(lastY), 'Configuration variables')

		lastY += 30

		config_ui_modified = []
		for c in config_ui:
			#print "config_ui for"
			temp = c.replace("YNOTDEFINED", str(lastY))
			temp = temp.replace("XNOTDEFINED", str(biggest_label_width+50))
			config_ui_modified.append(temp)
			lastY += 30	


	# Create file with string 'records'
	#file = open("out/"+asynPort+".db", "w")
	file = open(sys.argv[2]+"/"+asynPort+".db", "w")
	file.write(records)
	file.close()

	if len(dependentDevices) > 0:

		lastY += 30
		ui_relateddisplay = '<widget class="caRelatedDisplay" name="carelateddisplay"> \n <property name="geometry"> \n <rect> \n <x> 50 </x> \n <y> %s </y> \n <width> 230 </width> \n <height> 221 </height> \n </rect> \n </property>' % (lastY)

		labels = []
		files = []

		for dev in dependentDevices:
			index = findIndex(dev)
			nameIndex = findNameIndex(dev)

			if index == -1: #Index not found. Put 0 as default
				name = dev[nameIndex].text+"_0"
			else:
				name = dev[nameIndex].text+"_"+dev[index].text

			labels.append(name)
			files.append(name+".ui")

		ui_relateddisplay += '<property name="labels"> \n <string notr="true"> '

		first = True
		for l in labels:
			if first:
				ui_relateddisplay += '%s' % (l)
				first = False
			else:
				ui_relateddisplay += ';%s' % (l)

		ui_relateddisplay += '</string> \n </property> \n <property name="files"> \n <string notr="true"> '

		first = True
		for f in files:
			if first:
				ui_relateddisplay += '%s' % (f)		
				first = False
			else:
				ui_relateddisplay += ';%s' % (f)		

		ui_relateddisplay += '</string> \n </property> \n <property name="args"> \n <string notr="true">  '

		first = True
		for l in labels:
			if first:
				first = False
			else:
				ui_relateddisplay += ';'

		ui_relateddisplay += '</string> \n </property> \n </widget> \n'

		lastY += 251

	ui_header = '<ui version="4.0"> \n <class>MainWindow </class> \n <widget class="QMainWindow" name="MainWindow"> \n <property name="geometry"> \n <rect> \n <x> 0 </x> \n <width> %d </width> \n <height> %s </height> \n </rect> \n </property> \n <property name="windowTitle"> \n <string>MainWindow</string> \n </property> \n <widget class="QWidget" name="centralWidget"> \n' % (biggest_label_width+261,str(lastY + 30))
	ui_foot = '</widget> \n </widget> <customwidgets> \n <customwidget> \n <class>caMenu</class> \n <extends>QComboBox</extends> \n <header>caMenu</header> \n </customwidget> \n <customwidget> \n <class>caRelatedDisplay</class> \n <extends>QWidget</extends> \n <header>caRelatedDisplay</header> \n </customwidget> \n <customwidget> \n <class>caTextEntry</class> \n <extends>caLineEdit</extends> \n <header>caTextEntry</header> \n </customwidget> \n <customwidget> \n <class>caLineEdit</class> \n <extends>QLineEdit</extends> \n <header>caLineEdit</header> \n </customwidget> \n </customwidgets> \n <resources/> \n <connections/> \n </ui>'

	file = open(sys.argv[2]+"/"+asynPort+".ui", "w")
	#file.write(ui_header + ui_relateddisplay + ui + ui_foot)

	if len(dependentDevices) > 0:
		file.write(ui_header + ui_relateddisplay)
	else:
		file.write(ui_header)
	
	if len(status_ui) > 0:
		file.write(status_label)
		for s in status_ui_modified:
			file.write(s)

	if len(config_ui) > 0:
		file.write(config_label)
		for c in config_ui_modified:
			file.write(c)

	file.write(ui_foot)
	file.close()

	return dependentDevices

def parseVariable(var, portName):
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

	label_width = len(name)*9	
	
	ui = ""
	ui += '<widget class="QLabel" name="%s">\n <property name="geometry"> \n <rect> \n <x> 50 </x> \n <y> %s </y> \n <width> %d </width> \n <height> 15 </height> \n </rect> \n </property> <property name="text"> \n <string> %s </string> \n </property> \n </widget> \n' % (name, 'YNOTDEFINED', label_width,name)

	

	#Check type
	if status and len(enum) == 0:
		#new += "ai, "
		new += "stringin, "
		#dtyp = "asynFloat64"
		dtyp = "asynOctetRead"
		ui += '<widget class="caLineEdit" name="%s"> \n <property name="geometry"> \n <rect> \n <x> %s </x> \n <y> %s </y> \n <width> 211 </width> \n <height> 20 </height> \n </rect> \n </property> \n <property name="channel" stdset="0"> \n <string notr="true"> %s </string> \n </property> \n </widget>' %  ("$(DEVICE):"+name, 'XNOTDEFINED' ,'YNOTDEFINED', "$(DEVICE):"+name)
	elif not status and len(enum) == 0:
		#new += "ao, "
		new += "stringout, "
		#dtyp = "asynFloat64"
		dtyp = "asynOctetWrite"
		ui += '<widget class="caTextEntry" name="%s"> \n <property name="geometry"> \n <rect> \n <x> %s </x> \n <y> %s </y> \n <width> 211 </width> \n <height> 20 </height> \n </rect> \n </property> \n <property name="channel" stdset="0"> \n <string notr="true"> %s </string> \n </property> \n </widget>' %  ("$(DEVICE):"+name, 'XNOTDEFINED','YNOTDEFINED', "$(DEVICE):"+name)
	elif status and len(enum) > 0:
		new += "mbbi, "
		dtyp = "asynInt32"
		ui += '<widget class="caLineEdit" name="%s"> \n <property name="geometry"> \n <rect> \n <x> %s </x> \n <y> %s </y> \n <width> 211 </width> \n <height> 20 </height> \n </rect> \n </property> \n <property name="channel" stdset="0"> \n <string notr="true"> %s </string> \n </property> \n </widget>' %  ("$(DEVICE):"+name, 'XNOTDEFINED' ,'YNOTDEFINED', "$(DEVICE):"+name)
	elif not status and len(enum) > 0:
		new += "mbbo, "
		dtyp = "asynInt32"
		ui += '<widget class="caMenu" name="%s"> \n <property name="geometry"> \n <rect> \n <x> %s </x> \n <y> %s </y> \n <width> 211 </width> \n <height> 20 </height> \n </rect> \n </property> \n <property name="channel" stdset="0"> \n <string notr="true"> %s </string> \n </property> \n </widget>' %  ("$(DEVICE):"+name, 'XNOTDEFINED' ,'YNOTDEFINED', "$(DEVICE):"+name)

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

	return [new, ui, label_width]

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
