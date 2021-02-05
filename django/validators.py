import logging

from django.template.defaultfilters import filesizeformat

import magic  # module for file type validation
import requests
from main import settings
from rest_framework import serializers


'''
Using the `magic numbers` in the files signatures is optional,
so this is not a 100% safe method (there is no 100% safe method at all).
The validation is based on the assumption, that the uploaded file has the
correct signature. It is possible to change the signature of any file
manually.

`python-magic` cannot recognise all the MIME types, so those ones,
which it does not know are marked as `application/octet-stream`.

Some of the older MS doc, xls, ppt, msg formats are not recognised,
so `python-magic marks them as 'application/octet-stream.

Some of the MS doc, docx, xls, xlsx etc. files can be recognised as
`text/xml`, since they are based on the XML format.

All modern MS doc, docx, xls, xlsx etc. files are ZIP files
`application/zip`.

WARNING: Some filetypes might contain macros. We will need a virusscanner
in place for those.

References:
https://www.lifewire.com/mime-types-by-content-type-3469108
https://www.iana.org/assignments/media-types/media-types.xhtml
https://en.wikipedia.org/wiki/List_of_file_signatures
https://mimesniff.spec.whatwg.org/#understanding-mime-types
'''


class FileValidator:

    logger = logging.getLogger('validators.file-validator')
    error_messages = {
        'max_size': ('Ensure this file size is not greater than %(max_size)s.'
                     ' Your file size is %(size)s.'),
        'min_size': ('Ensure this file size is not less than %(min_size)s. '
                     'Your file size is %(size)s.'),
        'allowed_type': 'Files of type %(content_type)s are not allowed.',
        'virusscanner_malware': 'This file is possibly infected with malware.',
        'virusscanner_error': 'Issue connecting to virusscanner.',
    }

    def __init__(self, max_size=None, min_size=None, allowed_types=[]):
        self.max_size = max_size
        self.min_size = min_size
        self.allowed_types = allowed_types

    def __call__(self, data):
        '''Check if uploaded file satisfies the conditions:
            - max_size -- the maximum allowed file size
            - min_size -- the minimum allowed file size
            - allowed_type -- the allowed file MIME types
            - virus scanner returns 200

        :param bytearray data: bytes from a file
        :raises ValueError: if any of the conditions fail
        '''
        if self.max_size and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise serializers.ValidationError(self.error_messages['max_size'],
                                              params)

        if self.min_size and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise serializers.ValidationError(self.error_messages['min_size'],
                                              params)

        # Reset to first byte and save header data as variable
        data.seek(0)
        header = data.read(settings.HEADER_SIZE_MIME_RECOGNITION)
        data.seek(0)
        # Check if file matches allowed MIME-type.
        content_type = magic.from_buffer(header, mime=True)
        self.logger.info('Uploading file with MIME type: %s' % content_type)
        if content_type not in self.allowed_types:
            params = {'content_type': content_type}
            self.logger.error('MIME type not allowed')
            raise serializers.ValidationError(
                self.error_messages['allowed_type'],
                params,
            )

        # Reset to first byte
        data.seek(0)
        # Send all data to virusscanner endpoint
        r = requests.post(url=settings.VIRUSSCANNER_ENDPOINT_URL,
                          files={'file': ('file', data)},
                          verify=False)
        self.logger.info(r.status_code)
        if r.status_code == 406:
            self.logger.error('Malware has been found')
            raise serializers.ValidationError(
                self.error_messages['virusscanner_malware'])
        elif r.status_code != 200:
            self.logger.error(
                'Virus scanner down? Statuscode: %s' % r.status_code)
            raise serializers.ValidationError(
                self.error_messages['virusscanner_error'],
                code=500,
            )

        # If all checks passed, reset data to first byte again
        data.seek(0)
