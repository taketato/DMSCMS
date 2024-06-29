#!/bin/bash

echo "installing requirements for backend server"
pip install -r requirements.txt

echo "installing requirements for frontend server"
cd frontend
npm install
npm install react 
npm install mui
npm install jwt-decode
npm install react-router-dom
npm install @mui/material
npm install @mui/icons-material
npm install @emotion/react
npm install @emotion/styled
cd ../

echo "installing requirements for blockchain server"
sudo npm install ganache-cli -g

echo "successfully installed environment"


