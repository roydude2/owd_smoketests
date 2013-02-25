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


Some notes on running "run_tests" ...
-------------------------------------

1. The first time you execute "run_tests", it will install the latest Python 2.7 / ADB / Gaiatest and Marionette suites (plus make a few adjustments to them). This can take a few minutes, but should only happen the first time you run "run_tests" after cloning the repo each time.

2. You can ask "run_tests" to execute specific smoketests by passing it the test numbers from the Basic_smoketest spreadsheet:

   <pre>./run_tests 7 8 12 15</pre>

3. You will be prompted for any input values required by the tests you have chosen (if you specify none it will assume you want all tests).

   * If you these values are stored in the file ./tests_parameters/parameters, then you will not be prompted for them.
   * If you specify the number of the device itself for sms tests, then they may timeout (because as soon as the device sends a text, the response is recei
ved and read so the statusbar notification for that response never happens). It is advisable, therefore, to use the number of a different device fro sms
 tests.
