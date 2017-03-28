#!/usr/bin/env python
import os, StringIO, tempfile

from PyRTF.utils import RTFTestCase
from PyRTF.Elements import Document
from PyRTF.document.section import Section


class DocumentTestCase(RTFTestCase):
    def test_documentWrite(self):
        doc, section, styles = RTFTestCase.initializeDoc()

        fd, filename = tempfile.mkstemp(prefix='test-pyrtf', suffix='.rtf')
        os.close(fd)
        doc.write(filename)

        result = StringIO.StringIO()
        doc.write(result)

        assert open(filename, 'r').read() == result.getvalue()
        os.remove(filename)
