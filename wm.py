import os
import subprocess as sp

tmp_dir = os.path.join(os.environ.get('XDG_RUNTIME_DIR', '/tmp'), 'qoverview')

def get_window_ids(workspace):

	out = sp.check_output("wmctrl -l | awk '($2 != \"-1\") && ($2 == \"%s\") { print $1 }'" % workspace, shell=True)
	out = out.decode('utf-8')

	return [x.strip() for x in out.split('\n')][:-1]  # :-1 removes last element (which will be empty) from list

def get_window_name(win_id):

	out = sp.check_output("wmctrl -l | grep %s | awk '{$1=\"\"; $2=\"\";$3=\"\"; print $0}' | sed 's/^   //g'" % win_id, shell=True)

	return out.decode('utf-8').rstrip()

def close(win_id):

	sp.Popen(['xdotool', 'windowclose', win_id]).wait()

def activate(win_id):

	sp.Popen(['xdotool', 'windowactivate', win_id])

def get_num_workspaces():

	out = sp.check_output(['xdotool', 'get_num_desktops'])
	return int(out.decode('utf-8').rstrip())

def switch_workspace(workspace_num):

	sp.Popen(['xdotool', 'set_desktop', str(workspace_num)])

def get_current_workspace():

	try:
		res = int(sp.check_output(['xdotool', 'get_desktop']).decode('utf-8').rstrip())

	except sp.CalledProcessError:
		res = 0

	return res

def get_window_screenshot(win_id, filename):

	sp.Popen(['import', '-quiet', '-window', win_id, os.path.join(tmp_dir, filename + '.png')]).wait()
	return os.path.join(tmp_dir, filename + '.png')

def get_window_icon(win_id, filename):

	cmdline = 'xprop -id '+win_id+' -notype 32c _NET_WM_ICON | perl -0777 -pe \'@_=/\\d+/g; printf "P7\\nWIDTH %d\\nHEIGHT %d\\nDEPTH 4\\nMAXVAL 255\\nTUPLTYPE RGB_ALPHA\\nENDHDR\\n", splice@_,0,2; $_=pack "N*", @_; s/(.)(...)/$2$1/gs\' > ' + os.path.join(tmp_dir, filename + '.pam')
	sp.Popen(cmdline, shell=True).wait()
	sp.Popen(['convert', os.path.join(tmp_dir, filename + '.pam'), os.path.join(tmp_dir, filename + '.png')]).wait()
	return os.path.join(tmp_dir, filename + '.png')

def move_to_workspace(workspace, w_id):

	sp.Popen(['xdotool', 'set_desktop_for_window', w_id, str(workspace)]).wait()

def get_focused_window():

	return hex(int(sp.check_output(['xdotool', 'getactivewindow']).decode('utf-8').strip()))

def set_window_title(window, title):

	sp.Popen(['xdotool', 'set_window', '--name', title, window]).wait()

