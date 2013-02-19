#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json


class MockContact(dict):
    #
    # The key values here match the data structure in the contacts db
    # so that the json output of this mock can be inserted directly into db
    #
    def __init__(self):
        self.Roy = {
                "givenName" : "Roy",
                "familyName": "Collings",
                "name"      : "Roy Collings",
                "email"     : {"type": "", "value": "roy.collings@sogeti.com"},
                "tel"       : {"type": "Mobile", "value": "124356789"},
                "adr"       : {"streetAddress"    : "C/L'Test 13, 1/4",
                               "postalCode"       : "08001",
                               "locality"      : "Barcelona",
                               "countryName"   : "Espana"},
                "bday"      : "1972-04-13",
                "jobTitle"  : "Flamenco dancer",
                "comment"   : "Mock test contact Roy"
            }

        self.Contact_1 = {
                "givenName" : "John",
                "familyName": "Smith",
                "name"      : "John Smith",
                "email"     : {"type": "", "value": "john.smith@nowhere.com"},
                "tel"       : {"type": "Mobile", "value": "111111111"},
                "adr"       : {"streetAddress"    : "One Street",
                               "postalCode"       : "00001",
                               "locality"      : "City One",
                               "countryName"   : "Country One"},
                "bday"      : "1981-01-21",
                "jobTitle"  : "Runner number one",
                "comment"   : "Mock test contact 1"
            }

        self.Contact_2 = {
                "givenName" : "Wilma",
                "familyName": "Wiggle",
                "name"      : "Wilma Wiggle",
                "email"     : {"type": "", "value": "wilma.wiggle@nowhere.com"},
                "tel"       : {"type": "Mobile", "value": "222222222"},
                "adr"       : {"streetAddress"    : "Two Street",
                               "postalCode"       : "00002",
                               "locality"      : "City Two",
                               "countryName"   : "Country Two"},
                "bday"      : "1982-02-22",
                "jobTitle"  : "Dancer number two",
                "comment"   : "Mock test contact 2"
            }

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]
