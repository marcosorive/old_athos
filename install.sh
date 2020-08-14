echo "Installing utils for the installation...."
apt-get install -y curl unzip xvfb libxi6 libgconf-2-4 software-properties-common dirmngr
echo "Done."
echo "Installing Google Chrome..."
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get -y update
apt-get -y install google-chrome-stable
echo "Done."

echo "Installing chromedriver..."
wget https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver
echo "Done."

echo "Installing Mongodb..."
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
add-apt-repository 'deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main'
apt -y update
apt install mongodb-org
echo "Done"

echo "Starting Mongod..."
systemctl start mongod
systemctl enable mongod
echo "Done."

echo "Cleaning packages..."
apt-get purge -y curl unzip xvfb libxi6 libgconf-2-4 software-properties-common dirmngr
apt-get autoremove
echo "Done."

echo "Installing Python, pip  and dependencies"
apt install -y python3.7
apt-get install -y python3-pip
pip3 install --user pipenv
pipenv install
echo "Done."