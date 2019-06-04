echo Welcome to ShinkeyBot Linux
if ! pgrep python; then
   echo 'Starting Shinkeybot'
   cd /srv/www
   cd ShinkeyBot
   cd NeoCortex
   killall -q python
   rm -f running.wt
   python Brainstem.py >> neocortex.log &
else
   echo 'Shinkeybot is already running'
fi
