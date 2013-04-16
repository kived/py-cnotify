
from notify.signal cimport Signal

cdef class AbstractValueObject(object):
	cdef __weakref__
	
	cdef Signal __signal
	cdef int __flags
	
	cpdef object get(AbstractValueObject self)
	cpdef int set(AbstractValueObject self, object value)
	cpdef int _is_mutable(AbstractValueObject self)
	
	cdef Signal __get_changed_signal(AbstractValueObject self)
	cdef tuple _create_signal(AbstractValueObject self)
	
