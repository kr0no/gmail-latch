import time, latch
from mechanize import Browser

# GMAIL SETTINGS
USER = 'YOUR_GMAIL_USER'
PASSWD = 'YOUR_GMAIL_PASSWORD'

# LATCH SETTINGS
APP_ID = 'LATCH_APP_ID'
APP_SECRET = 'LATCH_APP_SECRET'
api = latch.Latch(APP_ID, APP_SECRET)

# Time beetwen auth checks in seconds
TIME = 3

# The AccountID we receive when we pair the device is saved in 'asd'.
# We read it, and if it has no content, we request the pairing code
f = open('account_id', 'r+')
accountId = f.read()
if(accountId == ''):
	print "Type your pairing code"
	pair_code = raw_input("> ")
	response = api.pair(pair_code)
	responseData = response.get_data()
	accountId = responseData["accountId"]
	f.write(accountId)
f.close()

# We use mechanize to enter in our gmail account
br = Browser()
br.set_handle_robots(False)
br.open('https://accounts.google.com/ServiceLogin?service=mail')
br.select_form(nr=0)
br.form["Email"] = USER
br.form["Passwd"] = PASSWD
br.submit()

# Infinite loop checking for unauthorized sessions
while True:
	time.sleep(TIME)
	br.open('https://mail.google.com/mail/u/0/?ui=2&ik=4b23d5edac&view=ac')
	br.select_form(nr=0)
	for control in br.form.controls:
		if(control.type == 'submit'):
			print '[+] Opened sessions detected. Checking Latch status...'
			status = api.status(accountId)
			statusData = status.get_data()
			try:
				if(statusData['operations'][APP_ID]['status'] == 'off'):
					print '[!] INTRUDER'
					br.submit()
				else:
					print '[+] Authorized'
			except:
				print 'Latch error (maybe an AccountId error, try to delete \'account_id\' content)'