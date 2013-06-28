# -*- coding: utf-8 -*-

#--------------------------------------------------------------------#
# This file is part of Py-cnotify.                                   #
#                                                                    #
# Copyright (C) 2007, 2008 Paul Pogonyshev.                          #
#                                                                    #
# This library is free software; you can redistribute it and/or      #
# modify it under the terms of the GNU Lesser General Public License #
# as published by the Free Software Foundation; either version 2.1   #
# of the License, or (at your option) any later version.             #
#                                                                    #
# This library is distributed in the hope that it will be useful,    #
# but WITHOUT ANY WARRANTY; without even the implied warranty of     #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU  #
# Lesser General Public License for more details.                    #
#                                                                    #
# You should have received a copy of the GNU Lesser General Public   #
# License along with this library; if not, write to the Free         #
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,        #
# Boston, MA 02110-1301 USA                                          #
#--------------------------------------------------------------------#


"""
cNotify package provides three main concepts: I{L{signals <signal>}}, I{L{conditions
<condition>}} and I{L{variables <variable>}}.  Signals are basically lists of callables
that can be I{emitted} and then will call all contained callables (I{handler} of a signal)
in turn.  Conditions are boolean values complemented with a signal that is emitted when
condition’s I{state} changes.  Variables are akin to conditions but can hold arbitrary
I{values}, not just booleans.  Conditions, unlike variables, can also be combined using
standard logic operators, like negation, conjunction and so on.

All three concepts provide separation between providers (writers, setters) and listeners
(readers, getters) of some entity.  Conditions and variables make the entity explicit—it
is a boolean state for the former and arbitrary Python object for the latter (though
derived variable classes can restrict the set of allowed values.)

Here is a quick example:

    >>> from cnotify.variable import *
    ... name = Variable ()
    ...
    ... import sys
    ... name.changed.connect (
    ...     lambda string: sys.stdout.write ('Hello there, %s!\\n' % string))
    ...
    ... name.value = 'Chuk'

Note that when setting the C{name} variable, you don’t need to know who, if anyone,
listens to changes to it.  Interested parties take care to express their interest
themselves and are informed upon a change automatically.

Here is a little more elaborate example with the same functionality (it requires U{PyGTK
<http://pygtk.org/>}):

    >>> from cnotify.variable import *
    ... import gtk
    ...
    ... name = Variable ()
    ...
    ... def welcome_user (name_string):
    ...     dialog = gtk.MessageDialog (None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
    ...                                 'Hello there, %s!' % name_string)
    ...     dialog.run ()
    ...     dialog.destroy ()
    ...
    ... name.changed.connect (welcome_user)
    ...
    ... def set_name_from_entry (entry):
    ...     name.value = entry.get_text ()
    ...
    ... window = gtk.Window ()
    ... window.set_title ('Enter name')
    ...
    ... entry = gtk.Entry ()
    ... entry.show ()
    ... window.add (entry)
    ...
    ... entry.connect ('activate', set_name_from_entry)
    ... window.connect ('destroy', lambda window: gtk.main_quit ())
    ...
    ... window.present ()
    ...
    ... gtk.main ()

Note that C{window} knows absolutely nothing about how changes to C{name} variable are
handled.  If you play with this example, you will notice one thing: pressing C{Enter} in
the main window twice doesn’t pop the welcoming dialog twice.  That is because both
conditions and variables emit their ‘changed’ signal I{only} when their state/value
actually changes, not on every assignment.

Now a final, quite complicated, example introducing conditions and some other features:

    >>> from cnotify.all import *
    ...
    ... pilots = Variable ()
    ... fuel   = Variable ()
    ...
    ... import sys
    ...
    ... pilots.changed.connect (
    ...     lambda pilots: sys.stdout.write ('Pilots are %s\\n' % pilots))
    ... fuel.changed.connect (
    ...     lambda amount: sys.stdout.write ('Got %d litres of fuel\\n' % amount))
    ...
    ... def ready_state_changed (ready):
    ...     if ready:
    ...         sys.stdout.write ('Ready to get off!\\n')
    ...     else:
    ...         sys.stdout.write ('Missing pilots or fuel\\n')
    ...
    ... ready = pilots.is_true () & fuel.predicate (lambda amount: amount > 0)
    ... ready.store (ready_state_changed)
    ...
    ... pilots.value = 'Jen and Jim'
    ... fuel.value   = 500
    ...
    ... fuel.value   = 0

First line of example shows a way to save typing by importing all package contents at
once.  Whether to use this technique is up to you.  Following lines up to C{ready = ...}
should be familiar.

Now let’s consider that assignment closer.  First, C{L{pilots.is_true ()
<variable.AbstractVariable.is_true>}} code creates a condition that is true depending on
C{pilots} value (true for non-empty sequences in our case.)  It is just a convenience
wrapper over C{L{AbstractVariable.predicate <variable.AbstractVariable.predicate>}}
method.  Now, the latter is also used directly in this line of code.  It creates a
condition that is true as long as variable’s value conforms to the passed in predicate.
In particular, C{fuel.predicate (lambda amount: amount > 0)} creates a condition that is
true if C{fuel}’s value is greater than zero.  Predicate conditions will recompute their
state each time variable’s value changes and that’s the point in using them.

Finally, two just constructed conditions are combined into a third condition using ‘and’
operator (C{&}).  This third condition will be true if and only if I{both} its term
conditions are true.  Conditions support four logic operations: negation, conjunction,
disjunction and xoring (with these operators: C{~}, C{&}, C{|} and C{^}.)  In addition,
each condition has C{L{if_else <condition.AbstractCondition.if_else>}} method, which is
much like Python’s C{if} operator.

The next line introduces one more new method: C{L{store
<base.AbstractValueObject.store>}}.  It is really just like connecting its only argument
to the ‘changed’ signal, except that it is also called once with the current state of the
condition (or value of a variable.)

The example should produce this output::

    Missing pilots or fuel
    Pilots are Jen and Jim
    Got 500 litres of fuel
    Ready to get off!
    Got 0 litres of fuel
    Missing pilots or fuel

Notable here is the output from C{ready_state_changed} function.  It is called once at the
beginning from the C{store} method with the state of C{ready} condition (then C{False}.)
Both later calls correspond to changes in C{ready}’s state.  When both C{pilots} and
C{fuel} variables are set, corresponding predicate conditions become true and so does the
C{ready} condition.  However, when one of the predicate conditions becomes false (as the
result of C{fuel} being set to zero), C{ready} turns false again.  Note that
C{ready_state_changed} is not called in between of setting C{pilots} and C{fuel} variable.
C{ready} state is recomputed, but since it remains the same, ‘changed’ signal is not
emitted.

G{packagetree}
"""

__docformat__ = 'epytext en'


# CONFIGURATION

__version__   = '0.3.2.1'
"""
Version of Py-cnotify, as a string.
"""

version_tuple = (0, 3, 2, 1)
"""
Version of Py-cnotify, as a tuple of integers.  It is guaranteed that version tuples of
later versions will compare greater that those of earlier versions.
"""

# /CONFIGURATION


# Local variables:
# mode: python
# python-indent: 4
# indent-tabs-mode: nil
# fill-column: 90
# End:
