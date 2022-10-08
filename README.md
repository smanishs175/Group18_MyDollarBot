# WalletBuddy
<hr>
<p align="center">
<a><img  height=560 width=1000 
  src="https://github.com/deekay2310/MyDollarBot/blob/c56b4afd4fd5bbfffea0d0a4aade58596a5cb678/docs/0001-8711513694_20210926_212845_0000.png" alt="Expense tracking made easy!"></a>
</p>
<hr>

![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
[![Python 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/smanishs175/WalletBuddy)
![GitHub](https://img.shields.io/badge/Language-Python-blue.svg)
![GitHub contributors](https://img.shields.io/github/contributors/deekay2310/SE21_HW2B_Group6)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5542548.svg)](https://doi.org/10.5281/zenodo.5542548)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
[![Build Status](https://app.travis-ci.com/deekay2310/MyDollarBot.svg?branch=main)](https://app.travis-ci.com/github/deekay2310/MyDollarBot)

<hr>

## About WalletBuddy

WalletBuddy is an easy-to-use Telegram Bot that assists you in recording your daily expenses on a local system without any hassle.  
With simple commands, this bot allows you to:
- Add/Record a new spending
- Show the sum of your expenditure for the current day/month
- Display your spendings plot : All expenses, Category expenses, Group Expenses
- Clear/Erase all your records
- Erase any spending details if you wish to

## Demo
https://user-images.githubusercontent.com/15325746/135395315-e234dc5e-d891-470a-b3f4-04aa1d11ed45.mp4

## Installation guide

The below instructions can be followed in order to set-up this bot at your end in a span of few minutes! Let's get started:

1. Set up your own server for deployment.

2. This installation guide assumes that you have already installed Python (Python3 would be preferred) and setup your own server.

3. Install git and add your account details using terminal.

4. Clone this repository to your local system at a suitable directory/location of your choice

5. Start a terminal session, and navigate to the directory where the repo has been cloned

6. Run the following command to install the required dependencies:
```
  pip3 install -r requirements.txt
```
7. Download and install the Telegram desktop application for your system from the following site: https://desktop.telegram.org/

8. Once you login to your Telegram account, search for "BotFather" in Telegram. Click on "Start" --> enter the following command:
```
  /newbot
```
9. Follow the instructions on screen and choose a name for your bot. Post this, select a username for your bot that ends with "bot" (as per the instructions on your Telegram screen)

10. BotFather will now confirm the creation of your bot and provide a TOKEN to access the HTTP API - copy this token for future use.

11. Paste the token copied in step 8 in the config.ini file under settings in ApiToken variable.

12. In the Telegram app, search for your newly created bot by entering the username and open the same. Once this is done, go back to the terminal session. Navigate to the directory containing the "main" folder inside your application code:
```
  run python3 main/main py
```
13. A successful run will generate a message on your terminal that says "TeleBot: Started polling." 

14. Post this, navigate to your bot on Telegram, enter the "/start" or "/menu" command, and you are all set to track your expenses!

## Running publicly available bot:

If you want to run publicly hosted bot then got to :
```
  https://t.me/niharrao_bot
```
send message to the bot named "sebot" and start managing your expanses using different functionalities.


<hr>
<p>--------------------------------------------------------------------------------------------------</p>
<p>Title:'WalletBuddy'</p>
<p>Version: '1.0'</p>
<p>Description: 'An easy to use Telegram Bot to track everyday expenses'</p>
<p>Authors:'Nihar, Shruti, Palash, Saksham, Manish'</p>
<p>--------------------------------------------------------------------------------------------------</p>
