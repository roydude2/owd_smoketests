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

<pre>
./run_tests
</pre>

... or specify particular test numbers, like this:

<pre>
./run_tests 7 8 21 40 41
</pre>


... and hopefully that's all you need to do. The device should run through some tests, at the end you'll get a response in the terminal for the test results.


Some notes on running "run_tests" ...
-------------------------------------

1. The first time you execute "run_tests", it will install Python 2.7 and ADB as well as re-installing the latest versions of Gaiatest and Marionette (plus make a few adjustments to them). This can take a few minutes, but should only happen the first time you run "run_tests" after cloning the repo each time.

2. You can ask "run_tests" to execute specific smoketests by passing it the test numbers from the ./docs/Basic_smoketest_GP_v04.xls spreadsheet:

<pre>./run_tests 7 8 12 15</pre>

3. You will be prompted for any input values required by the tests you have chosen (if you specify none it will assume you want all tests).

* If you these values are stored in the file ./tests_parameters/parameters, then you will not be prompted for them. You should keep a copy of this file so you can restore it each time you clone this repository.
* If you specify the number of the device itself for sms tests, then they may timeout (because as soon as the device sends a text, the response is received and read so the statusbar notification for that response never happens). It is advisable, therefore, to use the number of a different device for sms tests.


SMOKETESTS COVERED:
===================
<!--tests-->
<table>
  <tr>
    <th>Test Case</th><th>Description</th>
  </tr>
  <tr>
    <td  align=center>07</td><td  align=left>Create a contact via the contacts app.</td>
  </tr>
  <tr>
    <td  align=center>08</td><td  align=left>Edit a contact in the contacts app.</td>
  </tr>
  <tr>
    <td  align=center>09</td><td  align=left>Send an SMS to a contact from the contacts app.</td>
  </tr>
  <tr>
    <td  align=center>10</td><td  align=left>Send and receive an SMS via the messaging app.</td>
  </tr>
  <tr>
    <td  align=center>11</td><td  align=left>Take a picture with camera.</td>
  </tr>
  <tr>
    <td  align=center>12</td><td  align=left>Record a video and view it in the gallery app.</td>
  </tr>
  <tr>
    <td  align=center>13</td><td  align=left>Play recorded video in the video player app.</td>
  </tr>
  <tr>
    <td  align=center>14</td><td  align=left>Browse photos in gallery.</td>
  </tr>
  <tr>
    <td  align=center>16</td><td  align=left>Load a website via Wifi.</td>
  </tr>
  <tr>
    <td  align=center>17</td><td  align=left>Load a website via Cellular Data.</td>
  </tr>
  <tr>
    <td  align=center>20</td><td  align=left>Install a market installed hosted app.</td>
  </tr>
  <tr>
    <td  align=center>21</td><td  align=left>Launch market installed hosted app.</td>
  </tr>
  <tr>
    <td  align=center>22</td><td  align=left>Combination of 22 and 23 - Send and receive an email between hotmail accounts.</td>
  </tr>
  <tr>
    <td  align=center>24</td><td  align=left>Combination of 24 and 25 - Send and receive an email between gmail accounts.</td>
  </tr>
  <tr>
    <td  align=center>27</td><td  align=left>First time use screens.</td>
  </tr>
  <tr>
    <td  align=center>29</td><td  align=left>Killing apps via the homescreen.</td>
  </tr>
  <tr>
    <td  align=center>31</td><td  align=left>Launch a packaged app.</td>
  </tr>
  <tr>
    <td  align=center>32</td><td  align=left>Delete a packaged app.</td>
  </tr>
  <tr>
    <td  align=center>34</td><td  align=left>Add and view an event to an offline calendar in each calendar view.</td>
  </tr>
  <tr>
    <td  align=center>35</td><td  align=left>Add an alarm (will pause for < 1 minute while waiting for alarm to start).</td>
  </tr>
  <tr>
    <td  align=center>39</td><td  align=left>Install and launch an everything.me app.</td>
  </tr>
  <tr>
    <td  align=center>40</td><td  align=left>Import Facebook contacts from contacts app settings.</td>
  </tr>
  <tr>
    <td  align=center>41</td><td  align=left>Link a facebook contact.</td>
  </tr>
  <tr>
    <td  align=center>42</td><td  align=left>First time use screens - check ENGLISH keyboard.</td>
  </tr>
  <tr>
    <td  align=center>43</td><td  align=left>First time use screens - check PORTUGUESE keyboard.</td>
  </tr>
  <tr>
    <td  align=center>44</td><td  align=left>First time use screens - check SPANISH keyboard.</td>
  </tr>
</table>
