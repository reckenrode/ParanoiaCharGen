#!/usr/bin/env python

# (c) 2000 Copyright Mark Nottingham
# <mnot@pobox.com>
#
# This software may be freely distributed, modified and used,
# provided that this copyright notice remain intact.
#
# This software is provided 'as is' without warranty of any kind.

''' 
cgi_buffer is a library that may be used to improve performance of CGI
scripts in some circumstances, by applying HTTP mechanisms that are
typically not supported by them.

For more information:
  http://www.mnot.net/cgi_buffer/
'''

__version__ = "0.3"
error = "cgi_buffer error"
generate_etag = 1		# flag to generate an ETag
compress_content = 1	# flag to content-encode if appropriate

import sys, cStringIO, httpheaders, httpheadertypes, os, base64, md5, time
from copy import copy
from string import index, lower
try:
	import zlib, gzip
except:
	zlib = None


def init():
	''' Some slight setup '''
	sys.stdout = cStringIO.StringIO()
	sys.exitfunc = cleanup


def cleanup():
	'''
	Gather the contents of sys.stdout, do appropriate processing, and print
	the result to the *true* stdout.
	'''
	
	env = os.environ
	f = sys.stdout.tell()
	sys.stdout.seek(0)
	g = sys.stdout.read()
	sys.stdout = sys.__stdout__

	try:
		i = index(g, '\n\n')
	except ValueError:
		raise error, "Can't find end of HTTP Headers."
	try:
		headers = httpheaders.DemandHeaders(g[:i])
	except StandardError, why:
		raise error, "HTTP header parsing error: %s" % why
	body = g[i+2:]

	### content encoding
	if env.has_key('HTTP_ACCEPT_ENCODING') and compress_content and \
	 zlib and headers.content_type[:4] == 'text':
		accept_encoding = httpheadertypes.QValList(env['HTTP_ACCEPT_ENCODING'])
		for encoding in accept_encoding:
			if encoding == 'gzip' or encoding == 'x-gzip':
				headers.content_encoding.append(encoding)
				headers.vary.append('Accept-Encoding')
				body = _gzip_body(body)
				break

	### ETag conditional validation
	if generate_etag:
		etag = base64.encodestring(md5.new(body).digest())[:-1]
		headers.etag = etag
		if env.has_key('HTTP_IF_NONE_MATCH'):
			validators = httpheadertypes.ETagList(env['HTTP_IF_NONE_MATCH'])
			if etag in validators:
				print "Status: 304 Not Modified"
				headers.send_entity = 0
				print headers
				return

	# content length
	headers.content_length = len(body)

	# output
	sys.stdout.write("%s\r\n%s" % (headers, body))


def run_program(program_name):
	''' simple wrapper to run a program '''
	print os.popen(program_name).read()


def _gzip_body(i):
	# here's an ugly hack to make sure gzip file doesn't have time embedded
	tmptime = time.time
	time.time = lambda a=None:0
	sb = cStringIO.StringIO()
	gb = gzip.GzipFile(mode='wb', fileobj=sb, compresslevel=2)
	gb.write(i)
	gb.close()
	time.time = tmptime
	sb.seek(0)
	o = sb.read()
	sb.close()
	return o


if __name__ == '__main__':
	pass
else:
	init()
