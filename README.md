Instructions for setting up and running automated smoke tests.
==============================================================

1. Make sure your device has been flashed with an 'eng' build (the 'user' build won't allow Marionette to run and the tests won't work).

   <pre>
   sudo ./bin/flash_device
   </pre>


2. Make sure 'remote debugging' is *OFF* on your device:

   *Settings > Device Information > More Information >  Developer > Remote debugging*



RUNNING THE TESTS:
==================

1. Plug the device in :) 

2. Type:

    <pre>./run_tests</pre>


... and hopefully that's all you need to do. The device should run through some tests, at the end you'll get a response in the terminal for the test results.

*NOTE:* The first time you run this, it will install the latest Python 2.7 / ADB / Gaiatest and Marionette suites (plus make a few adjustments to them). This can take a few minutes, but should only happen the first time you run "run_tests" after cloning the repo each time.
