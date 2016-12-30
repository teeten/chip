#!/bin/sh

cp autopoweroff.py /usr/local/sbin
(cd /usr/local/sbin ; ln -s autopoweroff.py autopoweroffd)
cp autopoweroff.service /etc/systemd/system
ls -l /usr/local/sbin/autopoweroff* /etc/systemd/system/autopoweroff*
echo ""
systemctl daemon-reload
