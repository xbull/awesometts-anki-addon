# -*- coding: utf-8 -*-

# AwesomeTTS text-to-speech add-on for Anki
# Copyright (C) 2010-Present  Anki AwesomeTTS Development Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Service implementation for Baidu Translate's text-to-speech API
"""

from .base import Service
from .common import Trait

__all__ = ['Baidu']


VOICES = {
    'zh': "Chinese, English",
}


class Baidu(Service):
    """
    Provides a Service-compliant implementation for Baidu Translate.
    """

    __slots__ = []

    NAME = "Baidu Translate"

    TRAITS = [Trait.INTERNET]

    def desc(self):
        """Returns a short, static description."""

        return "Baidu Translate text2audio web API (%d voices)" % len(VOICES)
        

    def extras(self):
        """The Baidu Translate API requires an Access Token."""

        return [dict(key='tok', label="Access Token", required=True)]

    def options(self):
        """Provides access to voice only."""

        return [
            dict(
                key='voice',
                label="Voice",
                values=[(code, "%s (%s)" % (name, code))
                        for code, name
                        in sorted(VOICES.items(), key=lambda t: t[1])],
                transform=self.normalize,
            ),
            
            dict(key='speed',
                 label="Speed",
                 values=(-10, +10),
                 transform=lambda i: min(max(-10, int(round(float(i)))), +10),
                 default=0),
        ]

    def run(self, text, options, path):
        """Downloads from Baidu directly to an MP3."""

        self.net_download(
            path,
            [
                ('https://tsn.baidu.com/text2audio',
                 dict(tex=subtext, lan=options['voice'], cuid='1', ctp='1', tok=options['tok'], speed=options['speed']))
                for subtext in self.util_split(text, 300)
            ],
            require=dict(mime='audio/mp3', size=512),
        )
