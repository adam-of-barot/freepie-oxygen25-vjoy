# FreePIE script for mapping MIDI to vJoy for M-Audio Oxygen 25

# Map structure syntax for sliders/dials:
# map = [(midi index, vJoy index, axis name)]

# Map structure syntax for buttons:
# map = [(midi index, vJoy index)]
# button index is determined by enumerating the list

# ---- Define maps ----

slider_map = [
	(1,0,'x'),  # modulation wheel C17
	(41,0,'y'), # master volume C9
]

dial_map = [
	(17,0,'rx'),	#C1
	(18,0,'ry'),	#C2
	(19,0,'rz'),	#C3
	(20,0,'dial'),	#C4
	(21,1,'rx'),	#C5
	(22,1,'ry'),	#C6
	(23,1,'rz'),	#C7
	(24,1,'dial')	#C8
]

button_map = [
	(113,0), #C10 cycle
	(114,0), #C11 back
	(115,0), #C12 forward
	(116,0), #C13 stop
	(117,0), #C14 playback
	(118,0)  #C15 record
]

# ---- Define control functions ----

def control_slider(midi_idx):
	"""
	This function determines which MIDI slider/dial to assign to vJoy axis
	"""
	return midi[0].data.buffer[0] == midi_idx and filters.mapRange(midi[0].data.buffer[1], 0, 127, -17873, 17873)


def control_button(btn_idx, midi_idx, vJoy_idx):
	"""
	This function determines which MIDI button to assign to which vJoy button
	"""
	condition = midi[0].data.buffer[1] > 50  # buttons can either be in 0 or 127 position
	if (midi[0].data.buffer[0] == midi_idx):
		vJoy[vJoy_idx].setButton(btn_idx, condition)


# ---- Main "loop" ----

def update():

   # set sliders
	for s in slider_map:
		if midi[0].data.buffer[0] == s[0]:
			setattr(vJoy[s[1]], s[2], control_slider(s[0]))
	
	# set dials
	for d in dial_map:
		if midi[0].data.buffer[0] == d[0]:
			setattr(vJoy[d[1]], d[2], control_slider(d[0]))
	
	# set buttons
	for btn_idx, b in enumerate(button_map):
		control_button(btn_idx, *b)

	#diagnostics.watch(midi[0].data.channel)
	#diagnostics.watch(midi[0].data.status)
	#diagnostics.watch(midi[0].data.buffer[0])
	#diagnostics.watch(midi[0].data.buffer[1])
	#diagnostics.watch(vJoy[0].x)
	#diagnostics.watch(vJoy[0].y)
	#diagnostics.watch(vJoy[0].rx)
	#diagnostics.watch(vJoy[0].ry)
	#diagnostics.watch(vJoy[0].rz)
	#diagnostics.watch(vJoy[0].dial)
	#diagnostics.watch(vJoy[1].x)
	#diagnostics.watch(vJoy[1].y)
	#diagnostics.watch(vJoy[1].rx)
	#diagnostics.watch(vJoy[1].ry)
	#diagnostics.watch(vJoy[1].rz)
	#diagnostics.watch(vJoy[1].dial)


if starting:
	midi[0].update += update