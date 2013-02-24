Instructions for setting up and running automated smoke tests.
==============================================================

NOTE: Currently I have a copy of 'gaia_ui_tests' in here because I need to tweak certain elements
      of it (for example the latest release restarts the phone before each test, which was losing
      my phone's connection - I commented this out to make my tests work).
      When you run the tests, the script will install my version of gaiatest.


If you have any of these items already installed then try the tests with your installed version first.


(For the following, type the commands in a Linux terminal ...)

1. Make sure your device has been flashed with an 'eng' build (the 'user' build
   won't allow Marionette to run and the tests won't work).

   <pre>
   sudo bin/unagi_flash.get_file
   sudo bin/unagi_flash.flash_device
   </pre>


2. Make sure 'remote debugging' is *OFF* on your device:

   *Settings > Device Information > More Information >  Developer > Remote debugging*


3. PYTHON 2.7 (check first with "python -V" from the command line):

   <pre>
   sudo add-apt-repository ppa:fkrull/deadsnakes
   sudo apt-get update
   sudo apt-get install python2.7
   </pre>


4. Android Debug Bridge (adb):

   <pre>
   sudo add-apt-repository ppa:nilarimogard/webupd8
   sudo apt-get update
   sudo apt-get install android-tools-adb android-tools-fastboot
   </pre>



BEFORE YOU BEGIN:
=================

Run 

    ./setup

... to install and tweak gaiatest (some adjustments need to be made to it before running tests). 


RUNNING THE TESTS:
==================

1. Plug the device in. 

2. Type:

    <pre>./run_tests</pre>


... and hopefully that's all you need to do. The device should run through some tests, at the end you'll get a response in the terminal for the test results.

NOTE: The first time you run this, it will install the latest gaiatest and marionette suites (plus make a few adjustments to them). This can take a few minutes, but should only happen the first time you run "run_tests" after cloning the repo each time.
