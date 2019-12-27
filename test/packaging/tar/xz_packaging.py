#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

"""
This tests the SRC xz packager, which does the following:
 - create a tar package from the specified files
"""
import os.path
import TestSCons

python = TestSCons.python

test = TestSCons.TestSCons()
tar = test.detect('TAR', 'tar')
if not tar:
    test.skip_test('tar not found, skipping test\n')

# Windows 10 now supplies tar, but doesn't support xz compression
# assume it's just okay to check for an xz command, because don't
# want to probe the command itself to see what it supports
xz = test.where_is('xz')
if not xz:
    test.skip_test('tar found, but helper xz not found, skipping test\n')

xz_path = os.path.dirname(xz)

test.subdir('src')

test.write([ 'src', 'main.c'], r"""
int main( int argc, char* argv[] )
{
  return 0;
}
""")

test.write('SConstruct', """
DefaultEnvironment(tools=[])
Program( 'src/main.c' )
env=Environment(tools=['packaging', 'filesystem', 'tar'])

# needed for windows to prevent picking up windows tar and thinking non-windows bzip2 would work.
env.PrependENVPath('PATH', r'%s')

env.Package( PACKAGETYPE  = 'src_tarxz',
             target       = 'src.tar.xz',
             PACKAGEROOT  = 'test',
             source       = [ 'src/main.c', 'SConstruct' ] )
"""%xz_path)

test.run(arguments='', stderr=None)

test.must_exist('src.tar.xz')

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
