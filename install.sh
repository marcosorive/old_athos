echo "Installing utils for the installation...."
apt-get -qq -y install curl unzip xvfb libxi6 libgconf-2-4 software-properties-common dirmngr
echo "Done."
echo "Installing Google Chrome..."
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get -y -qq update
apt-get -y -qq install google-chrome-stable
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
apt -qq -y update
apt -qq install mongodb-org
echo "Done"

echo "Installing Python, pip  and dependencies"
apt -qq -y install python3.7
apt -qq -y install python3-pip
pip3 install --user pipenv
echo export PATH="$PATH:/root/.local/bin"
pipenv install
echo "Done."