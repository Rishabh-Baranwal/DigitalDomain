.PHONY: build


build:
	rm -rf build
	mkdir build
	mkdir build/bin
	mkdir build/lib
	cp ./src/pm.py ./build/bin
	chmod a+x ./build/bin/pm.py
	cp ./src/projman.py ./build/lib


