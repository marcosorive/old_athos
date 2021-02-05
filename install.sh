#!/bin/bash
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
apt -qq -y install chromium-chromedriver
echo "Done."

echo "Installing sqlite..."

echo "Done"

echo "Installing Python, pip  and dependencies"
apt -qq -y install python3.7
apt -qq -y install python3-pip
pip3 install --user pipenv
echo export PATH="$PATH:/root/.local/bin" >> ~/.bashrc
pipenv install
echo "Done."