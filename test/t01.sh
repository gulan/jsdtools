#/bin/sh

BD=$HOME/1/jsd-tools

rm -f /tmp/account.dot
./astjsd.py < $BD/account/account.jsd > /tmp/account.dot

diff $BD/account/account.dot /tmp/account.dot
