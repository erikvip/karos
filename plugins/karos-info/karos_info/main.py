"""
QuickReference for Rst
======================

This is a markup example: [b]Hello[/b] [i]world[/i]
And if i really want to write my code: &amp;bl; Hello world &amp;br;

Inline Markup
-------------

- *emphasis*
- **strong emphasis**
- `interpreted text`
- ``inline literal``
- reference_
- `phrase reference`_
- anonymous__
- _`inline internal target`

.. _top:

Internal crossreferences, like example_, or bottom_.

Grid
----

+------------+------------+-----------+
| Header 1   | Header 2   | Header 3  |
+============+============+===========+
| body row 1 | column 2   | column 3  |
+------------+------------+-----------+
| body row 2 | column 2   | column 3  |
+------------+------------+-----------+
| body row 3 | column 2   | column 3  |
+------------+------------+-----------+

Term list
---------

:Authors:
    Tony J. (Tibs) Ibbs,
    David Goodger
    (and sundry other good-natured folks)

.. _example:

:Version: 1.0 of 2001/08/08
:Dedication: To my father.

Definition list
---------------

what
  Definition lists associate a term with a definition.

how
  The term is a one-line phrase, and the definition is one or more paragraphs or
  body elements, indented relative to the term. Blank lines are not allowed
  between term and definition.


Block quotes
------------

Block quotes are just:

    Indented paragraphs,

        and they may nest.


Admonitions
-----------

.. warning::

    This is just a Test.

.. note::

    And this is just a note. Let's test some literal::

        $ echo 'Hello world'
        Hello world

Ordered list
------------

#. My item number one
#. My item number two with some more content
   and it's continuing on the second line?
#. My third item::

    Oh wait, we can put code!

#. My four item::

    No way.

.. _bottom:

Go to top_"""

from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, Screen
from os.path import dirname
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import DictProperty
from kivy.uix.rst import RstDocument

from karos import utils

import kivy
import sys


class karos_info(Screen):
    hue = NumericProperty(0)
    docbody = ObjectProperty()
    colors = DictProperty({
        #'background': '151619ff',
        'background': '00000000',
        'link': 'ce5c00ff',
        'paragraph': 'd0d0d0ff',
        'title': '204a87ff',
        'bullet': '000000ff'})    

    def __init__( self, **kwargs):
        self.name = "info"
        Logger.info("karos_info: init")
        Builder.load_file(dirname(__file__) + "/main.kv")
        super(karos_info, self).__init__(**kwargs)

    def build(self):
        self.docbody = """
System Information
==================

Versions
--------

:Python: {pyver}

:Kivy: {kivyver}


        """.format(
                pyver=sys.version.replace("\n", ""), 
                kivyver=kivy.__version__
        )

        return self