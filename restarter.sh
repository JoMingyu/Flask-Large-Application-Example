git pull 
kill $(lsof -i :80 | grep python | awk '{print $2}')
sudo -E python3 server.py