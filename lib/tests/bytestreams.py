"Unit tests for byte stream and formatting code."
from __future__ import with_statement

import unittest
from c64.formats import format_bytes, ByteStream


class FormatBytesTests(unittest.TestCase):
    def test_a_few_bytes(self):
        s = format_bytes('\x00\x00\x01\x01')
        self.assertEqual(s, '00 00 01 01')

    def test_exact_row(self):
        s = format_bytes('\x00\x00\x01\x01', 2)
        self.assertEqual(s, '00 00\n01 01')

    def test_rows_and_extra(self):
        s = format_bytes('\x00\x00\x01\x01\x00', 2)
        self.assertEqual(s, '00 00\n01 01\n00')


class ByteStreamTests(unittest.TestCase):
    sample_bytes = '\x01\x02\x03\x04\x05\x06'
    
    def test_init(self):
        "ByteStreams should be created correctly given a string."
        b = ByteStream(self.sample_bytes)
        self.assertEquals(self.sample_bytes, b.rest())
        
    def test_byte(self):
        "Reading bytes should behave as expected."
        b = ByteStream(self.sample_bytes)
        
        bytes = list()
        for i in range(len(self.sample_bytes)):
            bytes.append(b.byte())
            
        self.assertEquals([1,2,3,4,5,6], bytes)
        self.assert_(b.eof())
        
    def test_word(self):
        "Reading words should behave as expected."
        b = ByteStream(self.sample_bytes)
        
        words = list()
        for i in range(len(self.sample_bytes)/2):
            words.append(b.word())
        
        self.assertEquals([2*256+1, 4*256+3, 6*256+5], words)
        self.assert_(b.eof())
        
    def _read_until(self, until, keep, expected):
        b = ByteStream('adam michael vandenberg')
        
        words = list()
        while not b.eof():
            words.append(b.read_until(until, keep=keep))
        
        self.assertEquals(expected, words)
        self.assert_(b.eof())
        
    def test_read_until_char(self):
        self._read_until(' ', False, ['adam','michael','vandenberg'])
            
    def test_read_until_byte(self):
        self._read_until(ord(' '), False, ['adam','michael','vandenberg'])
            
    def test_read_until_char_keep(self):
        self._read_until(' ', True, ['adam ','michael ','vandenberg'])
            
    def test_read_until_byte_keep(self):
        self._read_until(ord(' '), True, ['adam ','michael ','vandenberg'])
            

if __name__ == "__main__":
    unittest.main()  
