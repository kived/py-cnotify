py-cnotify
==========

py-cnotify is a Cythonized fork of py-notify by Paul Pogonyshev (http://gna.org/projects/py-notify).


py-notify
=========

Py-notify is a Python package providing tools for implementing Observer programming pattern. These
tools include signals, conditions and variables.

Signals are lists of handlers that are called when signal is emitted. Conditions are basically boolean
variables coupled with a signal that is emitted when condition state changes. They can be combined
using standard logical operators (not, and, etc.) into compound conditions. Variables, unlike conditions,
can hold any Python object, not just booleans, but they cannot be combined.

All three main concepts support deriving by users. Conditions and variables even have derive_type() method
that can be used to subclass them in just a few lines of code, for instance to create a variable that
restricts its value's type.

Latest Py-notify versions can be found at the homepage: http://home.gna.org/py-notify/


Running Standard Tests
======================

Py-notify ships with a set of standard test cases. However, these test cases have not yet been modified
for py-cnotify. If you want to try running them, just execute

 `./run-tests.py`

in the top-level directory of the project.


Installation
============

The usual `./setup.py build; ./setup.py install` or just `./setup.py install` should build and install
py-cnotify. See file INSTALL for details.

You can also build a Debian package from this project. Run `dpkg-buildpackage -B` to build a binary package 
for your host machine. The package has been tested and is working on Ubuntu Precise Pangolin (12.04) and Raring 
Ringtail (13.04, beta release) on both i386 and amd64.


Reporting Bugs
==============

Use the GitHub issues system for bug reporting. Please include the following information in your bug report:
* Bug description and the way to reproduce the bug.
* Exception stack trace, if any.
* System information, most importantly Python and Cython versions.
* Test case if possible.
* Everything else you find relevant.

If the bug is present in Py-notify as well as py-cnotify, you can submit a bug to the original project as well:
  https://gna.org/bugs/?group=py-notify
Before submitting a bug to the original project, be sure to download and test with the latest SVN version
of Py-notify and verify that the bug is still present. Don't forget to check if the bug has been submitted already.


Copyrights and Licenses
=======================

All files from the original Py-notify project are copyrighted by Paul Pogonyshev, except as noted below or
in each specific file.

* File `setup.py` is explicitly put in Public Domain.
* File `benchmark/configobj.py` is copyright (c) 2005-2006 Michael Foord, Nicola Larosa and released under the terms of the BSD License.

All Cython modifications to the original files are copyrighted by Ryan Pessa.

All source files are licensed under the GNU Lesser General Public License version 3 or (at your option) any
later version.
