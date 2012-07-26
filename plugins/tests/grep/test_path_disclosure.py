'''
test_path_disclosure.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
import unittest

import core.data.kb.knowledgeBase as kb

from core.data.parsers.urlParser import url_object
from core.data.request.fuzzableRequest import fuzzableRequest as fuzzableRequest
from core.data.url.httpResponse import httpResponse as httpResponse
from plugins.grep.path_disclosure import path_disclosure


class test_path_disclosure(unittest.TestCase):

    def setUp(self):
        self.plugin = path_disclosure()
        kb.kb.cleanup()
        self.url = url_object('http://www.w3af.com/')
        self.request = fuzzableRequest(self.url, method='GET')

    def tearDown(self):
        self.plugin.end()
            
    def test_path_disclosure(self):
        res = httpResponse(200, 'header body footer' , {'Content-Type':'text/html'}, self.url, self.url)
        self.plugin.grep( self.request, res )
        infos = kb.kb.getData('path_disclosure', 'path_disclosure')
        self.assertEquals( len(infos), 0)
    
    def test_path_disclosure_positive(self):
        res = httpResponse(200, 'header /etc/passwd footer' , {'Content-Type':'text/html'}, self.url, self.url)
        self.plugin.grep( self.request, res )
        
        infos = kb.kb.getData('path_disclosure', 'path_disclosure')
        self.assertEquals( len(infos), 1 )
        
        path = infos[0]['path']
        self.assertEqual( path, '/etc/passwd' )
        