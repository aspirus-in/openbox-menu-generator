from xdg import DesktopEntry
import os
import subprocess
import sys
from collections import defaultdict

def getIdentify(text):
	return text.strip().strip(' \t\n').replace(' ', '-').replace('\t', '-').lower()

def findCategory(cat_list):
	cats = ['Game',
	        'Utility',
	        'System',
	        'Graphics',
	        'Office',
	        'Development',
	        'Audio',
	        'Video',
	        'Network',]
	for i in cat_list:
		if i in cats:
			return i
	return 'Others'

def parseDesktopFile(file_whole_path):
	dfile = DesktopEntry.DesktopEntry(file_whole_path)
	if not dfile.getNoDisplay():
		return [dfile.getName(), findCategory(dfile.getCategories()), file_whole_path.split('/')[-1]]	
	else:
		return None

TABS = 0

def printf(text):
	global TABS
	for i in text.split('\n'):
		print(('  ' * TABS) + i)

def createItemComm(name, comm):
	printf(f'''<item label="{name}">
  <action name="Execute">
    <command>{comm}</command>
  </action>
</item>''')

def startMenu(menu_id, name):
	global TABS
	printf(f'<menu id="{menu_id}" label="{name}">')
	TABS += 1

def endMenu():
	global TABS
	TABS -= 1
	printf('</menu>')

def startConfig():
	global TABS
	printf('<openbox_menu xmlns="http://openbox.org/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://openbox.org/                 file:///usr/share/openbox/menu.xsd">')
	TABS += 1
	startMenu('root-menu', 'Openbox 3')

def endConfig():
	global TABS
	endMenu()
	TABS -= 1
	printf('</openbox_menu>')

def createPipeMenu(menu_id, name, comm):
	printf(f'<menu id="{menu_id}" label="{name}" execute="{comm} "/>')

def createSeparator():
	printf('<separator/>')

def createLabel(label):
	printf(f'<separator label="{label}"/>')

def templateDesktopMenu(path='/usr/share/applications'):
	dfiles = [x for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x)) and '.desktop' in x]
	dfiles_list = []
	for dfile in dfiles:
		dfile = parseDesktopFile(os.path.join(path, dfile))
		if dfile != None:
			dfiles_list.append(dfile)
	dfiles_dict = defaultdict(list)
	for i in dfiles_list:
		dfiles_dict[i[1]].append([i[0], i[2]])
	for cat in dfiles_dict:
		startMenu(getIdentify(cat), cat)
		for dfile in dfiles_dict[cat]:
			createItemComm(dfile[0], f'''gtk-launch {dfile[1]}''')
		endMenu()

def templateFlatpaks():
	flapak_ids = subprocess.check_output(['flatpak', 'list', '--app', '--columns=application']).decode('UTF-8').split('\n')
	flapak_names = subprocess.check_output(['flatpak', 'list', '--app', '--columns=name']).decode('UTF-8').split('\n')
	i = 0
	while i < len(flapak_ids):
		if flapak_ids[i] != '':
			createItemComm(flapak_names[i], f'flatpak run {flapak_ids[i]}')
		i += 1

def parse_config(conf):
	startConfig()
	i = 0
	while i < len(conf):
		key = conf[i].strip().strip('\t')
		if key[0] == '[' and key[-1] == ']':
			createLabel(key[1:-1])
		elif ':' in conf[i]:
			name = conf[i].split(':')[0].strip(' \t')
			comm = conf[i].split(':')[1].strip(' \t')
			createItemComm(name, comm)
		elif '{' in conf[i]:
			name = conf[i][:-1].strip(' \t')
			startMenu(getIdentify(name), name)
		elif key == '}':
			endMenu()
		elif key == '!dmenu':
			templateDesktopMenu()
		elif key == '!flatpaks':
			templateFlatpaks()
		elif key == '---':
			createSeparator()
		else:
			raise SyntaxError
		i += 1

	endConfig()

try:
	with open(sys.argv[1], 'r') as conf_file:
		conf_file = conf_file.readlines()
		i = 0
		while i < len(conf_file):
			conf_file[i] = conf_file[i].strip('\n')
			i += 1
		parse_config(conf_file)
except IndexError:
	print('Error: Pass a config file')
except FileNotFoundError:
	print('Error: Config file does not exist')