
# ls -la /usr/local/lib/
# ls -la /usr/local/include/
# cat Setup
# otool -L `find . -name imageext.so`
# otool -L `find . -name image.so`
# otool -L /usr/local/opt/sdl_image/lib/libSDL_image-1.2.0.dylib


# Removes any X11R6 stuff so that png headers are not picked up by accident.
sed 's/-I\/usr\/X11R6\/include //g' Setup > Setup.new
mv Setup.new Setup

# Makes for i386 and x86_64.
CXXFLAGS="-arch i386 -arch x86_64" CFLAGS="-arch i386 -arch x86_64" LDFLAGS="-arch i386 -arch x86_64" $PYTHON_EXE setup.py install -noheaders
CXXFLAGS="-arch i386 -arch x86_64" CFLAGS="-arch i386 -arch x86_64" LDFLAGS="-arch i386 -arch x86_64" $PYTHON_EXE setup.py bdist_wheel

# This copies in the .dylib files that are linked to the .so files.
# It also rewrites the .so file linking options. https://pypi.python.org/pypi/delocate
$PIP_CMD install delocate twine
delocate-wheel -v dist/*.whl
$PYTHON_EXE upload_pypi.py
