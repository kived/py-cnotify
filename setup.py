#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Py-cnotify.
#
# Unlike the rest of Py-cnotify, it is explicitely put in Public Domain.  Use as you
# please.


# In particular, we heavily use True and False, there are uses of enumerate(), file coding
# is explicitly set etc.

REQUIRED_PYTHON_VERSION = (2, 6)



import sys
import os
import re


if sys.version_info[:3] < REQUIRED_PYTHON_VERSION:
	sys.exit ('%s: Python version %s is required'
			  % (sys.argv[0],
				 '.'.join ([str (subversion) for subversion in REQUIRED_PYTHON_VERSION])))



if os.path.dirname (sys.argv[0]):
	os.chdir (os.path.dirname (sys.argv[0]))

if not os.path.isfile (os.path.join ('cnotify', 'all.py')):
	sys.exit ("%s: cannot find '%s', strange..."
			  % (sys.argv[0], os.path.join ('cnotify', 'all.py')))



try:
	version_file = open ('version')

	try:
		version = version_file.readline ().strip ()
	finally:
		version_file.close ()

except IOError:
	sys.exit ('%s: error: %s' % (sys.argv[0], sys.exc_info () [1]))



def configure (version):
	configuration_parameters = { 'version_string': version,
								 'version':		tuple (map (lambda string: int (string),
															   version.split ('.'))) }

	# This can be much simplified with Python 2.5 `with' statement, once that version is
	# required.

	try:
		template_file   = None
		output_file_in  = None
		output_file_out = None

		try:
			template_file	= open (os.path.join ('cnotify', '__init__.py.in'))
			result_line_list = []
			in_configuration = False

			for line in template_file:
				if re.search ('# *CONFIGURATION *$', line):
					in_configuration = True
				elif re.search ('# */CONFIGURATION *$', line):
					in_configuration = False
				else:
					if in_configuration:
						line = line % configuration_parameters

				result_line_list.append (line)

		finally:
			if template_file is not None:
				template_file.close ()

		output_file_name = os.path.join ('cnotify', '__init__.py')

		try:
			try:
				output_file_in = open (output_file_name, 'r')
			except IOError:
				# Cannot open, so ignore.
				pass
			else:
				if list (output_file_in) == result_line_list:
					return

		finally:
			if output_file_in is not None:
				output_file_in.close ()

		try:
			output_file_out = open (output_file_name, 'w')
			output_file_out.writelines (result_line_list)

		finally:
			if output_file_out is not None:
				output_file_out.close ()

	except IOError:
		sys.exit (str (sys.exc_info () [1]))



configure (version)



long_description = \
"""
Py-notify is a Python package providing tools for implementing `Observer programming
pattern`_.  These tools include signals, conditions and variables.

Signals are lists of handlers that are called when signal is emitted. Conditions are
basically boolean variables coupled with a signal that is emitted when condition state
changes. They can be combined using standard logical operators (*not*, *and*, etc.) into
compound conditions. Variables, unlike conditions, can hold any Python object, not just
booleans, but they cannot be combined.

For more verbose introduction, please refer to the tutorial_.

.. _Observer programming pattern:
   http://en.wikipedia.org/wiki/Observer_pattern

.. _tutorial:
   http://home.gna.org/py-notify/tutorial.html
"""

classifiers = ['Topic :: Software Development :: Libraries :: Python Modules',
			   'Intended Audience :: Developers',
			   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
			   'Development Status :: 4 - Beta',
			   'Operating System :: OS Independent',
			   'Programming Language :: Python',
			   'Programming Language :: C']

from distutils.core import setup, Extension

# -----------------------------------------------------------------------------
# Determine on which platform we are

platform = sys.platform

# Detect Python for android project (http://github.com/kivy/python-for-android)
ndkplatform = os.environ.get('NDKPLATFORM')
if ndkplatform is not None and os.environ.get('LIBLINK'):
	platform = 'android'
kivy_ios_root = os.environ.get('KIVYIOSROOT', None)
if kivy_ios_root is not None:
	platform = 'ios'
if os.path.exists('/opt/vc/include/bcm_host.h'):
	platform = 'rpi'

# -----------------------------------------------------------------------------
# Cython check
# on python-for-android and kivy-ios, cython usage is external
have_cython = False
if platform in ('ios', 'android'):
	print('\nCython check avoided.')
else:
	try:
		# check for cython
		from Cython.Distutils import build_ext as _build_ext
		have_cython = True
	except ImportError:
		print('\nCython is missing, it is required for compiling aeris2!\n\n')
		raise

if not have_cython:
	from distutils.command.build_ext import build_ext as _build_ext

# copied from kivy
class CythonExtension(Extension):
	def __init__(self, *args, **kwargs):
		Extension.__init__(self, *args, **kwargs)
		self.cython_directives = {
			'c_string_encoding': 'utf-8',
			'profile': 'USE_PROFILE' in os.environ,
			'embedsignature': 'USE_EMBEDSIGNATURE' in os.environ}
		# XXX with pip, setuptools is imported before distutils, and change
		# our pyx to c, then, cythonize doesn't happen. So force again our
		# sources
		self.sources = args[1]

def make_cy_ext(filename):
	modname = filename.replace('.pyx', '').replace('/', '.')
	srcname = filename if have_cython else (filename[:-4] + '.c')
	ext = CythonExtension(modname, [srcname])
	return ext

import fnmatch
def find_cy_ext(path):
	ext = []
	for root, dirnames, filenames in os.walk(path):
		for filename in fnmatch.filter(filenames, '*.pyx'):
			ext.append(make_cy_ext(os.path.join(root, filename)))
	return ext

class build_ext (_build_ext):

	def build_extension (self, extension):
		_build_ext.build_extension (self, extension)

		if not self.inplace and os.name == 'posix':
			filename		= self.get_ext_filename (extension.name)
			link_filename   = filename
			target_filename = os.path.join (self.build_lib, filename)

			recursion_scan  = os.path.split (filename) [0]

			if hasattr (os, 'symlink'):
				if (	os.path.islink (link_filename)
					and os.path.realpath (link_filename) == os.path.abspath (target_filename)):
					return

			while recursion_scan:
				recursion_scan  = os.path.split (recursion_scan) [0]
				target_filename = os.path.join  (os.pardir, target_filename)

			try:
				os.remove (link_filename)
			except:
				# Ignore all errors.
				pass

			if hasattr (os, 'symlink'):
				try:
					os.symlink (target_filename, link_filename)
				except:
					# Ignore all errors.
					pass
			else:
				# FIXME: Copy the library then.
				pass


gc_extension = Extension (name	= 'cnotify._gc',
						  sources = [os.path.join ('cnotify', '_gc.c')])

#from functools import partial
#path = partial(os.path.join, 'cnotify')
#cython_extensions = [
#	Extension(name='cnotify.signal', sources=[path('signal.pyx')]),
#	Extension(name='cnotify.base', sources=[path('base.pyx')]),
#	Extension(name='cnotify.bind', sources=[path('bind.pyx')]),
#	Extension(name='cnotify.condition', sources=[path('condition.pyx')]),
#	Extension(name='cnotify.mediator', sources=[path('mediator.pyx')]),
#	Extension(name='cnotify.utils', sources=[path('utils.pyx')]),
#	Extension(name='cnotify.variable', sources=[path('variable.pyx')])
#]
cython_extensions = find_cy_ext('cnotify')

setup (name			 = 'py-cnotify',
	   version		  = version,
	   description	  = 'An unorthodox implementation of Observer programming pattern.',
	   long_description = long_description,
	   author		   = 'Ryan Pessa',
	   author_email	 = 'ryan@essential-elements.net',
	   url			  = 'http://github.com/kived/py-cnotify/',
	   download_url	 = 'http://github.com/kived/py-cnotify/',
	   license		  = "GNU Lesser General Public License v3",
	   classifiers	  = classifiers,
	   packages		 = ['cnotify'],
	   ext_modules	  = [gc_extension] + cython_extensions,
	   cmdclass		 = { 'build_ext': build_ext })



# Local variables:
# mode: python
# python-indent: 4
# indent-tabs-mode: nil
# fill-column: 90
# End:
