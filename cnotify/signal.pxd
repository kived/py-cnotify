
cdef class _AbstractAccumulator(object):
	pass

cdef class _AnyAcceptsAccumulator(_AbstractAccumulator):
	pass

cdef class _AllAcceptAccumulator(_AbstractAccumulator):
	pass

cdef class _LastValueAccumulator(_AbstractAccumulator):
	pass

cdef class _ValueListAccumulator(_AbstractAccumulator):
	pass

cdef class AbstractSignal(object):
	cdef __weakref__
	
	cpdef int has_handlers(self)
	cpdef int count_handlers(self)
	
	cdef do_connect(self, handler)
	cdef int do_connect_safe(self, handler)
	
	cdef int _get_emission_level(self)
	cdef int _is_emission_stopped(self)
	
	cpdef int stop_emission(self)
	
	cpdef collect_garbage(self)
	
	cpdef object _additional_description(self, formatter)
	
	cpdef str __to_string(self, strict)
	

cdef class Signal(AbstractSignal):
	cdef list _handlers
	cdef object _blocked_handlers
	cdef object __accumulator
	cdef int __emission_level

cdef class CleanSignal(Signal):
	pass
