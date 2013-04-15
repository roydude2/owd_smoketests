Instructions for setting up and running automated smoke tests.
==============================================================

<b>1.</b> Clone and install the OWD_TEST_TOOLKIT repository (https://github.com/roydude/OWD_TEST_TOOLKIT).

<b>2.</b> Clone and install *this* repository, changing the ./run_tests.sh script to point to the location of your OWD_TEST_TOOLKIT installation.

<b>3.</b> Type:

<pre>
./run_tests.sh
</pre>

... or specify particular test numbers, like this:

<pre>
./run_tests 7 8 21 40 41
</pre>

For more details, please refer to the README.md for OWD_TEST_TOOLKIT.


<!--testcoverage-->
TESTS COVERED
=============
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
</table>
