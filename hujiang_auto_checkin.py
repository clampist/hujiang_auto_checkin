#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# +-----------------------------------------------------------------------------
# | File: hujiang_auto_checkin.py
# | Author: clampist
# | E-mail: clampist[at]gmail[dot]com
# | Created: 2012-09-16
# | Last modified: 2012-09-18
# | Description:
# |     auto checkin for hujiang
# | Copyrgiht (c) 2012 by clampist. All rights reserved.
# | License: GPLv3
# +-----------------------------------------------------------------------------

import re
import os
import sys
import urllib
import urllib2
import datetime
import cookielib
import subprocess

def check(response):
    """Check whether checkin is successful

    Args:
        response: the urlopen result of checkin

    Returns:
        If first time checkin would return '打卡成功，本次打卡共赚得 XX 沪元！已连续打卡XX天。'
        If already checkin, return a string '今日已打卡'
        If not, return False
    """
    #re.S：Make the '.' special character match any character at all, including a newline;
    # without this flag, '.' will match anything except a newline.
    pattern = re.compile(r'<div id="Tips_pnlNotice" class="tips_succ">(.*?)</div>', re.S)
    result = pattern.search(response)
    if result:
        return result.group(1).strip()
    pattern = re.compile(r'<span id="litCardNotice" class="gray">(.*?)</span>')
    result = pattern.search(response)
    if result:
        return result.group(1)
    return False

def main():
    """Main process of auto checkin
    """
    # Get log file
    LOG_DIR = os.path.join(os.path.expanduser("~"), '.log')
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    LOG_PATH = os.path.join(LOG_DIR, 'hujiang_auto_checkin.log')
    f = LOG_FILE = file(LOG_PATH, 'a')
    print >>f # add a blank space to seperate log

    # Get email|username and password
    if len(sys.argv) != 3:
        subprocess.call('notify-send -i error "[Error] Please input email|username & password as sys.argv!"', shell=True)
        print >>f, '[Error] Please input email|username & password as sys.argv!'
        print >>f, datetime.datetime.now()
        print '[Error] Please input email|username & password as sys.argv!'
        return
    email = sys.argv[1]
    password = sys.argv[2]

    # Init
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)

    # Login
    login_url = 'http://m.yeshj.com/login/'
    login_data = urllib.urlencode({'__VIEWSTATE':'/wEPDwUKLTE2OTkzMzY3NmRk', 'txtUserName':email, 'txtPassword':password, 'btnLogin':'登录',})
    login_headers = {'Referer':'http://m.yeshj.com/login/', 'User-Agent':'Opera/9.80',}   #Mozilla/5.0
    login_request = urllib2.Request(login_url, login_data, login_headers)
    login_response = urllib2.urlopen(login_request).read()

    # Checkin
    checkin_pattern = re.compile(r'<p class="normal"><input type="submit" name="btnDoCard" value="打卡领沪元" id="btnDoCard" />')
    checkin_result = checkin_pattern.search(login_response)
    if not checkin_result:
        # Checkin Already | Login Failed
        result = check(login_response)
        if result:
            subprocess.call('notify-send -i info "[Already] Checkin Already! ' + email +' '+ result + '"', shell=True)
            print >>f, '[Already] Checkin Already!', email, result
            print '[Already] Checkin Already!', email, result
        else:
            subprocess.call('notify-send -i error "[Error] Login Failed! ' + email + '"', shell=True)
            print >>f, '[Error] Login Failed!', email
            print '[Error] Login Failed!', email
        print >>f, datetime.datetime.now()
        return

    checkin_url = 'http://m.yeshj.com'
    checkin_data = urllib.urlencode({'__VIEWSTATE':'/wEPDwUKMTI5MTEzNDIxMWRk', 'btnDoCard':'打卡领沪元', 'txtIngContent':'',})
    checkin_headers = {'Referer':checkin_url, 'User-Agent':'Opera/9.80',}
    checkin_request = urllib2.Request(checkin_url, checkin_data, checkin_headers)
    checkin_response = urllib2.urlopen(checkin_request).read()

    # Result
    result = check(checkin_response)
    if result:
        subprocess.call('notify-send -i notification-message-email "[Success] Checkin Succeed! ' + email +' '+ result + '"', shell=True)
        print >>f, '[Success] Checkin Succeed!', email, result
        print '[Success] Checkin Succeed!', email, result
    else:
        subprocess.call('notify-send -i error "[Error] Checkin Failed!"', shell=True)
        print >>f, '[Error] Checkin Failed!'
        print '[Error] Checkin Failed!'
    print >>f, datetime.datetime.now()

if __name__=='__main__':
    main()
