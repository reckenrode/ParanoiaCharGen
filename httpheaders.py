#!/usr/bin/env python

# (c) 2000 Copyright Mark Nottingham
# <mnot@pobox.com>
#
# This software may be freely distributed, modified and used,
# provided that this copyright notice remain intact.
#
# This software is provided 'as is' without warranty of any kind.

'''
HTTP Header Parsing and Representation

The Headers() class wraps the HTTP Header Types, allowing easy and automated
access to them. It can be instantiated with an argument of either a
rfc822.Message instance, or a string containing headers to be parsed. 

Once the headers have been parsed (or an empty instance has been created), 
each header can be accessed as an attribute. Dashes ('-') in the header's
name should be converted to underscores ('_'), and the names are not 
case-sensitive.

Depending on a particular header's type, it may be accessed as a string,
integer, list or dictionary; for full details, look at the header's doc
string.

The headers may be printed by calling the __repr__ method.

Finally, the putheaders() method can be used to pass the headers back
to the specified httplib object, using its putheader() method.

The DemandHeaders class operates in a similar manner, except that headers are
only parsed if they are modified.

Note that although the header classes attempt to format their contents
correctly, they do not enforce HTTP compliance; the user should be familiar
with the specification (RFC 2616).
'''

import rfc822, sys, re
from string import lower, join, split, replace
from UserDict import UserDict
from httpheadertypes import *


__version__ = "0.61"
DATA = intern('data')
SEND_ENTITY = intern('send_entity')

entity_headers = [
	'Allow', 
	'Content-Encoding', 
	'Content-Language', 
	'Content-Length',
	'Content-Location',
	'Content-MD5',
	'Content-Range',
	'Content-Type',
	'Expires',
	'Last-Modified',
]

linesplitter = re.compile("(?:\r\n)|\n")
starting_whitespace = re.compile("^\s")

class Headers(UserDict):
	'''
	Contains a dictionary of Header instances, keyed by header name
	(case-insensitive).

	Can be instantised with a rfc822.Message object, or text of the headers,
	as the argument.
	'''

	def __init__(self, message=None):		
		UserDict.__init__(self)
		self.send_entity = 1
		if message != None:
			self.parse(message)

	def parse(self, message):
		if isinstance(message, rfc822.Message):
			header_list = message.headers
		else:
			header_list = linesplitter.split(message)

		prev_header = None
		for line in header_list:
			if starting_whitespace.search(line):
				value = strip(line)
				if prev_header:
					self.data[prev_header] = self.data[prev_header] + value
					continue
				else:
					self.handle_exception('parse orphan line', line)

			try:
				k, v = split(line, ":", 1)
				header_name, value = get_header_name(strip(k)), strip(v)
				if self.data.has_key(header_name) and \
				  isinstance(self.data[header_name], List):
					self.data[header_name] = self.data[header_name] + value
				else:
					self.data[header_name] = \
					  header_names.get(header_name, UnknownHeader)(value)
				prev_header = header_name
			except StandardError, msg:
				self.handle_exception('parse', line)

	def __getitem__(self, key):
		header_name = get_header_name(key)
		if not self.data.has_key(header_name):
			self.data[header_name] = \
			  header_names.get(header_name, UnknownHeader)()
		return self.data[header_name]

	def __setitem__(self, key, item):
		header_name = get_header_name(key)
		self.data[header_name] = \
		  header_names.get(header_name, UnknownHeader)(item)

	def __delitem__(self, key):
		del self.data[get_header_name(key)]

	def __getattr__(self, key):
		return self[replace(key, '_', '-')]
		
	def __setattr__(self, key, item):
		if key in [DATA, SEND_ENTITY]:
			self.__dict__[key] = item
		else:
			self[replace(key, '_', '-')] = item

	def __delattr__(self, key):
		del self[replace(key, '_', '-')]

	def has_key(self, key):
		return self.data.has_key(get_header_name(key))
	
	def get(self, key, default):
		return self.data.get(get_header_name(key), default)
	
	def __str__(self):
		return repr(self)
		
	def __repr__(self):
		o = []
		for header, obj in self.data.items():
			if not self.send_entity and header in entity_headers:
				continue
			try:
				if obj._is_foldable:
					val = repr(obj)
					if val:
						o.append("%s: %s" % (header, val))
				else:
					for line in obj.data:
						val = repr(line)
						if not val: continue
						o.append("%s: %s" %(header, val))
			except StandardError, args:
				self.handle_exception('repr', header)
		o.append('')	# last header's CRLF
		return join(o, "\r\n") 

	def putheaders(self, httpobj):
		''' put contained headers into httpobj using its putheader() meth. '''
		for header, obj in self.data.items():
			httpobj.putheader(header, repr(obj))

	def handle_exception(self, what, info):
		'''
		Handles parsing and repr errors (with bad headers or values). 
		Raise an exception to stop processing; to continue, log the error
		as you wish.
		'''
		exception = sys.exc_info()
		exception[1].args = (exception[1].args, info)
		raise exception[1]



#################################

class DemandHeaders(Headers):
	'''
	Headers are only parsed on demand - more efficient if you don't access
all headers, but need to output them.
'''

	def __init__(self, message=None):
		Headers.__init__(self, message=None)
		self.data = _DemandHeaderDict()
		if message != None:
			self.parse(message)

	def parse(self, message):
		if isinstance(message, rfc822.Message):
			header_list = message.headers
		else:
			header_list = linesplitter.split(message)

		prev_header = None
		for line in header_list:
			if starting_whitespace.search(line):
				value = strip(line)
				if prev_header:
					self.data.data[prev_header].append(value)
					continue
				else:
					self.handle_exception('parse orphan line', line)
			try:
				k, v = split(line, ":", 1)
				header_name, value = get_header_name(strip(k)), strip(v)
				prev_header = header_name
				if self.data.data.has_key(header_name):
					self.data.data[header_name].append(value)
				else:
					self.data[header_name] = [value]
			except StandardError, msg:
				self.handle_exception('parse', line)

	def __repr__(self):
		o = []
		for header in self.data.data.keys():
			obj = self.data[header]
			if not self.send_entity and header in entity_headers:
				continue
			if type(obj) is type([]):
				for hdr in obj:
					o.append("%s: %s" % (header, hdr))
			else:
				try:
					if obj._is_foldable:
						o.append("%s: %s" % (header, repr(obj)))
					else:
						for line in obj.data:
							o.append("%s: %s" % (header, repr(line)))
				except Exception, args:
					self.handle_exception('repr', header)
		o.append('')
		return join(o, "\r\n")


class _DemandHeaderDict(UserDict):
	def __getitem__(self, header_name):
		hdrlist = self.data[header_name]
		if type(hdrlist) is type([]):
			if issubclass(header_names.get(header_name, UnknownHeader), List):
				self.data[header_name] = \
				  header_names.get(header_name, UnknownHeader)(hdrlist[0])
				for value in hdrlist[1:]:
					self.data[header_name] = self.data[header_name] + value
			else:
				self.data[header_name] = \
				  header_names.get(header_name, UnknownHeader)(hdrlist[-1])
		return self.data[header_name]
		
	def get(self, key, failobj=None):
		if self.data.has_key(key):
			return self[key]
		else:
			return failobj
