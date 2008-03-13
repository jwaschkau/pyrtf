#!/usr/bin/env python
import sys

from adytum.util.sourceforge.base import login

filename, sfID = sys.argv[1:]
host = 'http://sourceforge.net'
loginURL = 'https://sourceforge.net/account/login.php'
formURL = '%s/project/admin/svn_migration.php?group_id=%s' % (host, sfID)
browser = login(loginURL, credFile='sourceforge_creds_test')

# submit the uploaded svn dump file
browser.open(formURL)
form = browser.getForm(name='migration')
form.getControl(name='src_path_type3').value = filename
form.getControl(name='button').click()
