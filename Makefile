
.PHONY: build clean

build:
	python setup.py build_ext -i

clean:
	find . -name '*.pyx' | while read pyx; do ppyx=`dirname $$pyx`/`basename $$pyx .pyx`; rm $$ppyx.c $$ppyx.so 2>/dev/null ||:; done
	find . -name '*.pyc' -exec rm {} \; ||:
	find . -name '*.so' -delete ||:
	find . -name '*.o' -delete ||:
