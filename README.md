Instructions for setting up and running automated smoke tests.
==============================================================

If you have any of these items already installed then try the tests with your installed version first.


(For the following, type the commands in a Linux terminal ...)

1. Make sure your device has been flashed with an 'eng' build (the 'user' build 
   won't allow Marionette to run and the tests won't work).

    sudo bin/unagi_flash.get_file
    sudo bin/unagi_flash.flash_device


2. PYTHON 2.7 (check first with "python -V" from the command line):

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python2.7


3. Python 'setuptools':
    
    sudo apt-get install python-setuptools


4. Android Debug Bridge (adb):

    sudo add-apt-repository ppa:nilarimogard/webupd8
    sudo apt-get update
    sudo apt-get install android-tools-adb android-tools-fastboot

	

RUNNING THE TESTS:
==================

1. Plug the device in.

2. In the "owd_smoketests" directory, type:

    ./run_tests
    
    
... and hopefully that's all you need to do. The device should run through some tests, at the end you'll
get a response in the terminal for the test results.
