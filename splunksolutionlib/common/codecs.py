# Copyright 2016 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''
This modules contains simple interfaces for File compression and decompression.
'''

import gzip
import cStringIO as StringIO
import zipfile

__all__ = ['GzipHandler',
           'ZipHandler']


class GzipHandler(object):
    '''
    Class for handling gzip-formatted string content.
    '''

    # Error messages
    ERR_INVALID_FORMAT = 'File is not gzip format.'

    def __init__(self):
        pass

    @classmethod
    def check_format(cls, data):
        '''Validate `data` whether it is in gzip format.

        Bytes 0 and 1 should be (per RFC 1952):
        data[0] = 31 (0x1f), data[1] = 139 (0x8b).

        :param data: data to check.
        :returns: True if it is in gzip format else False.
        :rtype: ``bool``
        '''

        return data[0:2] == '\x1f\x8b'

    @classmethod
    def decompress(cls, data):
        '''Decompress gzip-compressed data `data`.

        It will perform basic validation, then return the decompressed
        data or raises ValueError exception for invalid `data`.

        :param data: gzip-compressed data to decompress.
        :returns: decompressed data.
        :rtype: ``string``

        :raises ValueError:
            with error cls.ERR_INVALID_FORMAT for `data` is not in gzip format.
        '''

        if not cls.check_format(data):
            raise ValueError(cls.ERR_INVALID_FORMAT)

        return gzip.GzipFile(fileobj=StringIO.StringIO(data),
                             mode='rb').read()


class ZipHandler(object):
    '''
    Class for handling zip files.
    '''

    # Error messages
    ERR_EXCESS_FILES = 'Zip files containing multiple files not supported by this handler.'
    ERR_EXTRACT_ERROR = 'Unknown exception when extracting zip file.'
    ERR_INVALID_FORMAT = 'File is not zip format.'
    ERR_SIZE_MISMATCH = 'Zip file size does not match actual size.'

    def __init__(self):
        pass

    @classmethod
    def check_format(cls, data):
        '''Validate `data` whether it is in zip format.

        :param data: data to check.
        :returns: True if it is in zip format else False.
        :rtype: ``bool``
        '''

        return zipfile.is_zipfile(StringIO.StringIO(data))

    @classmethod
    def decompress(cls, data):
        '''Decompress zip-compressed data `data`.

        It will perform basic validation, then return the decompressed
        data or raises ValueError exception with error message.

        :param data: zip-compressed data to decompress.
        :returns: decompressed data.
        :rtype: ``string``

        :raises ValueError: with error message of
            cls.ERR_INVALID_FORMAT for `data` is not in zip format,
            cls.ERR_EXCESS_FILES for `data` contains multiple files,
            cls.ERR_SIZE_MISMATCH for `data` is not complete
        '''

        if not cls.check_format(data):
            raise ValueError(cls.ERR_INVALID_FORMAT)

        fh = StringIO.StringIO(data)
        decompressor = zipfile.ZipFile(fh)

        files = decompressor.infolist()
        if len(files) > 1:
            raise ValueError(cls.ERR_EXCESS_FILES)
        else:
            try:
                text = decompressor.read(files[0].filename)
            except:
                raise ValueError(cls.ERR_EXTRACT_ERROR)

        if len(text) != files[0].file_size:
            raise ValueError(cls.ERR_SIZE_MISMATCH)

        return text
