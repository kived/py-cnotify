
from cnotify.base cimport AbstractValueObject
from cnotify.condition cimport AbstractCondition

cdef class AbstractVariable(AbstractValueObject):
	cpdef AbstractCondition predicate(self, object predicate)

cdef class AbstractValueTrackingVariable(AbstractVariable):
	cdef object __value
	
	cpdef object get(AbstractValueTrackingVariable self)
	cpdef int _set(AbstractValueTrackingVariable self, object value)

cdef class Variable(AbstractValueTrackingVariable):
	cpdef int set(Variable self, object value)

