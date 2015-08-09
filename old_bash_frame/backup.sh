#!/bin/bash
tar -zcf backup_frame$( date +%F ) /var/spool/cron/crontabs/ /home/frame/
scp backup_frame$( date +%F ) ram@big:Desktop/
