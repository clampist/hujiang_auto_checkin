hujiang_auto_checkin
====================

hujiang auto checkin

support desktop notification and log file

also could add to crontab to autorun

crontab.example

    # replace /path/to/hujiang_auto_checkin.py with the real path
    # replace USERNAME and PASSWORD with email|username and password
    # env DISPLAY=:0.0 support notify
    6 */8 * * * env DISPLAY=:0.0 python /path/to/hujiang_auto_checkin.py USERNAME PASSWORD

