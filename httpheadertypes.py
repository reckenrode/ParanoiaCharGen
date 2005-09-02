#!/usr/bin/env python

# (c) 2000 Copyright Mark Nottingham
# <mnot@pobox.com>
#
# This software may be freely distributed, modified and used,
# provided that this copyright notice remain intact.
#
# This software is provided 'as is' without warranty of any kind.


'''
HTTP Header Types

This module contains the GenericHeader class, which can be (and is) 
subclassed to define the behaviour of a HTTP header. The class which
handles a particular header's representation is determined by the
header_names dictionary.

Each of the classes has the same basic interface:

* a parse() method - which will parse the raw header payload fed to it (and
  raise errors as necessary)
* a data dictionary - which allows access to the raw data after parsing
  (although most operations may be performed directly upon the object)
* a __repr__ method  - to print the data correctly in the Header's format

If the object is instantiated with an 'instr' argument, it is parsed
automatically. If it is instantiated with a 'data' argument, that value is
inserted into the data dictionary.

The original header before parsing, if any, is available as the 'raw'
attribute. 

Many of the headers are Lists, which are comma-seperated. Because the List
class is a subclass of the UserList object, it can be accessed like a normal
list. The same holds true for the Dict class, with respect to dictionaries.

Each class has a short __doc__ string that describes any special attributes
or behaviours.

the get_header_name function returns the canonical capitalisation of the
header name fed to it, if available, or a capitalied version if not.


TODO
- QValList - sort / get_best
- Warning = list of (int str quostr quohttpdate) ; (currently List)
- Expect = list of token[=qs] [;param] OR 100-continue ; (currently List)
- digest authorization
- Set-Cookie only takes the last one. Stupid !@#%$ Netscape spec!
- Range is a pretty pitiful implementation so far.
- Content-Range  ; (currently Str)
'''

import time, re, rfc822, urlparse, base64
from string import lower, join, strip, split, replace, capitalize
from operator import add, sub, mul, div, neg
from UserList import UserList
from UserDict import UserDict


__version__ = "0.61"
DATA = intern('data')

### patterns for splitting 
commapat = re.compile(r"""
	(?:,\s*|^)
	(
	(?:
	"(?:\\"|[^"])*"	
	|
	[^,"]+
	)*
	)
""", re.VERBOSE)
def splitoncomma(instr):
	if not instr: return []
	return commapat.findall(instr)	

semipat = re.compile(r"""
	(?:;\s*|^)
	(
	(?:
	"(?:\\"|[^"])*"	
	|
	[^;"]+
	)*
	)
""", re.VERBOSE)
def splitonsemi(instr):
	if not instr: return []
	return semipat.findall(instr)



class GenericHeader:
	'''
Base class for HTTP Headers. Should be subclassed.
'''

	def __init__(self, instr=None):
		''' 
		    Initialize a header; can take:
		      instr - a string to be parsed
		      data - parsed data to be instantiated into 
            only one of these should be specified.
		'''
		# keep the raw input string in case we need it later
		self.raw = instr
		# flag whether multiple headers can be comma-folded into a single
		# header per RFC2616; Set-Cookie, for instance, can't be.
		self._is_foldable = 1
		# flag simple type; when processing, if input data is same type as
		# self.data, it's considered processed.
		self._is_simple = 1
		if instr is not None:
			self.parse(instr)
	def __setattr__(self, attr, val):
		'''
		    Set an attribute.
		    If attr is 'data', it will be run through ._screen().
			Otherwise, can set arbitrary attributes.
		'''
		if attr == DATA and hasattr(self, DATA):
			self.__dict__[DATA] = self._screen(val)
		else:
			self.__dict__[attr] = val
	def __add__(self, other):
		self.__dict__[DATA] = self.data + self._screen(other)
		return self
	def __radd__(self, other):
		return add(self._screen(other), self.data)
	def __sub__(self, other):
		self.__dict__[DATA] = self.data - self._screen(other)
		return self
	def __rsub__(self, other):
		return sub(self._screen(other), self.data)
	def __cmp__(self, other):
		return cmp(self.data, self._screen(other))
	def __nonzero__(self):
		if self.data: return 1
		else: return 0
	def _screen(self, inp):
		''' Decide whether the input needs to be processed '''
		if isinstance(inp, self.__class__):
			return inp.data
		elif type(inp) is type(self.data) and self._is_simple:
			return inp
		else:
			return self._process(inp)
	def _process(self, inp):
		''' 
		   Transform raw input into suitable header data. Should
		   be overridden.
	  	'''
		return inp
	def parse(self, instr):
		''' Parse an input string into header data '''
		self.__dict__[DATA] = self._screen(instr)
	def __repr__(self):
		''' Output the data in HTTP header format. Can be overridden. '''
		return str(self.data)


class Int(GenericHeader):
	'''
Integer.
'''
	def __init__(self, instr=None):
		self.data = 0
		GenericHeader.__init__(self, instr)
	def __mul__(self, other):
		self.__dict__[DATA] = self.data * self._screen(other)
		return self
	def __rmul__(self, other):
		return mul(self._process(other), self.data)
	def __div__(self, other):
		self.__dict__[DATA] = self.data / self._screen(other)
		return self
	def __rdiv__(self, other):
		return div(self._process(other), self.data)
	def __int__(self):
		return int(self.data)
	def __float__(self):
		return float(self.data)
	def __abs__(self):
		return abs(self.data)
	def __neg__(self):
		return neg(self.data)
	def _process(self, inp):
		return int(inp)


class Str(GenericHeader):
	'''
String (case-sensative)
'''
	def __init__(self, instr=None, case_sens=1):
		self._case_sens = case_sens
		self.data = ''
		GenericHeader.__init__(self, instr)	
	def __getitem__(self, i):
		return self.data[i]
	def __getslice__(self, i, j):
		return self.data[i:j]
	def _process(self, inp):
		if self._case_sens:
			return str(inp)
		else:
			return lower(inp)


class Str_i(Str):
	'''
String (case-insensitive)
'''
	def __init__(self, instr=None, case_sens=0):
		Str.__init__(self, instr, case_sens)
		self._is_simple = 0


class List(GenericHeader, UserList):
	'''
List of case-sensitive strings.
'''
	def __init__(self, instr=None, objtype=Str):
		self._objtype = objtype		# type of contained object
		self.data = []					### this used be UserList()
		GenericHeader.__init__(self, instr)
		self._is_simple = 0
	def __setattr__(self, key, item):
		if key == DATA:
			self.__dict__[DATA] = self._process(item)
		else:
			self.__dict__[key] = item
	def __setslice__(self, i, j, other):
		i = max(i, 0); j = max(j, 0)
		self.__dict__[data][i:j] = self._process(other)
	def __setitem__(self, i, item):
		self.__dict__[data][i] = self._objtype(item)
	def append(self, item):
		self.__dict__[DATA].append(self._objtype(item))
	def insert(self, i, item):
		self.__dict__[DATA].insert(i, self._objtype(item))
	def _process(self, inp):
		if type(inp) is type(''):
			inp = map(strip, splitoncomma(inp))
		l = []
		for header in inp:
			if not header: continue
			l.append(self._objtype(header))
		return l
	def __repr__(self):
		return join(map(repr, self.data), ', ')


class List_i(List):
	'''
List of case-insensitive strings.
'''
	def __init__(self, instr=None):
		List.__init__(self, instr, Str_i)
	

class Dict(GenericHeader, UserDict):
	'''
Dictionary of key=value pairs, separated by commas. Keys are 
case-insensitive; values are not. If possible, the value will be
converted to an integer.
'''
	def __init__(self, instr=None, splitfunc=splitoncomma, joinchar=','):
		self.data = {}
		self._splitfunc = splitfunc
		self._joinchar = joinchar
		GenericHeader.__init__(self, instr)
		self._is_simple = 0
	def __setattr__(self, k, v):
		GenericHeader.__setattr__(self, k, v)
	def _process(self, inp):
		# type checking...
		o = self._splitfunc(inp)
		res = {}
		for i in o:
			try:
				name, value = split(strip(i), '=', 1)
				name = lower(name)
				value = unquotestring(value)
				### special cases for Cache-Control
				if name in ['private', 'no-cache']:
					value = map(get_header_name, self._splitfunc(value))
				try:
					value = int(value)
				except:
					pass
			except ValueError:
				name, value = lower(strip(i)), None
			res[name] = value
		return res		
	def __repr__(self):
		o = []
		for k, v in self.data.items():
			k = lower(k)
			if v == None:
				o.append(k)
			else:
				if k in ['private', 'no-cache'] and type(v) == type([]):
					v = '"%s"' % (
					  join(map(get_header_name, v), self._joinchar + " "))
				elif type(v) is type(''):
					v = quotestring(v)
				o.append("%s=%s" % (k,v))
		return join(o, self._joinchar + " ")


class SemiDict(Dict):
	def __init__(self, instr=None):
		Dict.__init__(self, instr, splitonsemi, ';')


class SemiDictList(List):
	def __init__(self, instr=None):
		List.__init__(self, instr, SemiDict)


class ETag(Str):
	'''
ETag. The value set will be quoted (and escaped, if need be). The .weak
attribute denotes a weak validator.
'''
	def __init__(self, instr=None):
		self.weak = 0
		Str.__init__(self, instr)
	def _process(self, inp):
		self.weak = 0
		if inp[:2] == 'W/':
			self.weak = 1
			inp = inp[2:]
		return unquotestring(inp)
	def __repr__(self):
		weak_str = ''
		if self.weak:
			weak_str = "W/"
		return "%s%s" % (weak_str, quotestring(self.data, force=1))


class ETagList(List):
	'''
List of ETags.
'''
	def __init__(self, instr=None):
		List.__init__(self, instr, ETag)


class HttpDate(Int):
	'''
HTTP Date - available as seconds since Epoch.
'''
	def __init__(self, instr=None):
		GenericHeader.__init__(self, instr)
	def _process(self, instr):
		parsed = rfc822.parsedate(instr)
		try:
			return timegm(parsed)
		except:
			return None
	def __repr__(self):
		try:
			return time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(self.data))		
		except:
			return "0"


class Uri(GenericHeader, UserList):
	'''
URI - available as urlparse 6-tuple.
'''
	def __init__(self, instr=None):
		self.data = ('', '', '', '', '', '')
		GenericHeader.__init__(self, instr)
	def _process(self, instr):
		return urlparse.urlparse(instr)
	def __repr__(self):
		return urlparse.urlunparse(self.data)


class Param(Str_i):
	'''
Parameterized data. primary data available as object instance, 
parameters available as a dictionary in the .params attribute.
Param keys are case-insensitive, values are case-sensitive.
'''
	def __init__(self, instr=None):
		self.params = {}
		Str_i.__init__(self, instr)
		self._is_simple = 0
	def _process(self, inp):
		self.params = {}
		try:
			data, args = split(inp, ';', 1)
		except ValueError:
			return inp
		for param in splitonsemi(args):
			try:
				attr, value = split(param, "=", 1)
				self.params[lower(attr)] = unquotestring(value)
			except ValueError:
				self.params[lower(param)] = None
		return data
	def __repr__(self):
		o, out = [], ''
		for k,v in self.params.items():
			if v == None:
				o.append(k)
			else:
				o.append("%s=%s" % (k, quotestring(v)))
		if o:
			out = '; ' + join(o, '; ')
		return "%s%s" % (self.data, out)


class ParamList(List):
	def __init__(self, instr=None):
		List.__init__(self, instr, Param)


class QValList(ParamList):
	'''
List of parameterised data. If an item has a 'q' parameter associated with 
it, that will determine its relative value.
'''
	def __init__(self, instr=None):
  		ParamList.__init__(self, instr)


class Header(Str):
	'''
Canonicalized HTTP header name.
'''
	def __init__(self, instr=None):
		Str.__init__(self, instr)
		self._is_simple = 0
	def _process(self, inp):
		return(get_header_name(inp))


class HeaderList(List):                ### list of headers, or *
	'''
List of HTTP headers in canonical format.
'''
	def __init__(self, instr=None):
		List.__init__(self, instr, Header)


class Challenge(Dict):
	'''
HTTP Authorization challenge. Currently, only Basic is supported.
Attributes:
  .scheme : scheme used (should be set to 'basic')
  .realm : authentication realm
'''
	def __init__(self, instr=None):
		Dict.__init__(self, instr)
	def _process(self, inp):
		try:
			scheme, args = split(inp, None, 1)
		except:
			scheme, args = inp, None			
		self.data['scheme'] = lower(scheme)
		return Dict._process(self, args)
	def __repr__(self):
		if lower(self.data['scheme']) == 'basic':
			o = []
			for k,v in self.data.items():
				if lower(k) == 'scheme': continue
				o.append("%s=%s" % (k, quotestring(v)))
			return "%s %s" % (
			  capitalize(lower(self.data['scheme'])), join(o, ', '))
		else:
			raise StandardError, "Digest Auth not supported yet."			  


class Credentials(Dict):
	'''
HTTP Authorization credentials. Currently, only Basic is supported.
Attributes:
  .scheme : scheme used (should be set to 'basic')
  .username : username
  .password : password
'''
	def __init__(self, instr=None):
		Dict.__init__(self, instr)
	def _process(self, inp):
		scheme, args = split(inp, None, 1)
		self.data['scheme'] = lower(scheme)
		if self.data['scheme'] == 'basic':
			self.data['username'], self.data['password'] = split(
			  base64.decodestring(args), ':', 1)
		else:
			raise StandardError, "Digest Auth not supported yet."
		return None
	def __repr__(self):
		if lower(self.data['scheme']) == 'basic':
			return "%s %s" % (
			  capitalize(lower(self.data['scheme'])), 
			  base64.encodestring(join((self.data['username'], 
			  self.data['password']), ':'))[:-1])
		else:
			raise StandardError, "Digest Auth not supported yet."


class Range(List):
	'''
Range request. Specifier is available on .specifier attribute (should be
'bytes'); ranges are in the List itself.
'''
	def __init__(self, instr=None):
		self.specifier = 'bytes'
		List.__init__(self, instr, Str)
	def _process(self, inp):
		specifier, args = split(inp, '=', 1)
		self.specifier = lower(specifier)
		return List._process(self, args)
	def __repr__(self):
		return "%s=%s" % (self.specifier, List.__repr__(self))


class HttpDateorInt(HttpDate, Int):
	'''
Either a HTTP Date or Integer. If a date is represented as seconds since
the epoch, the .is_date attribute should be true; if it represents delta
seconds, it should be false.
'''
	def __init__(self, instr=None):
		self.is_date = 0
		HttpDate.__init__(self, instr)
		self._is_simple = 0
	def _process(self, inp):
		try:
			return Int._process(self, inp)
		except:
			self.is_date = 1
			return HttpDate._process(self, inp)
	def __repr__(self):
		if self.is_date:
			return HttpDate.__repr__(self)
		else:
			return Int.__repr__(self)


class Validator(HttpDate, ETag):
	'''
Either a HTTP Date or an ETag. If a date is represented, the .is_date
attribute should be true; otherwise, it should be false.
'''
	def __init__(self, instr=None):
		self.is_date = 0
		self.weak = 0
		HttpDate.__init__(self, instr)
	def _process(self, inp):
		self.is_date = 1
		try:
			return HttpDate._process(self, inp)
		except:
			self.is_date = 0
			self.__dict__[DATA] = ''
			return ETag._process(self, inp)
	def __repr__(self):
		if self.is_date:
			return HttpDate.__repr__(self)
		else:
			return ETag.__repr__(self)


class SetCookie(SemiDictList):
	'''
A SemiDictList that's not foldable, because of the !@#$ cookie spec.
'''
	def __init__(self, instr=None):
		SemiDictList.__init__(self, instr)
		self._is_foldable = 0
		

class UnknownHeader(Str):
	'''
Generic holder for unknown headers; treats them as strings, and doesn't
fold them.
'''
	def __init__(self, instr=None):
		Str.__init__(self, instr)
#		self._is_foldable = 0


### header_names: this is where the headers are actually associated with
### an HeaderType, and shown with their canonical spelling.

header_names = {'Accept': QValList,
				'Accept-Charset': QValList,
				'Accept-Encoding': QValList,
				'Accept-Language': QValList,
				'Accept-Ranges': List_i,
				'Age': Int,
				'Allow': List,
				'Authorization': Credentials,
				'Cache-Control': Dict,
				'Connection': List_i,
				'Content-Encoding': List_i,
				'Content-Language': List_i,
				'Content-Length': Int,
				'Content-Location': Uri,
				'Content-MD5': Str,
				'Content-Range': Str,
				'Content-Type': Param,
				'Cookie': Dict,
				'Date': HttpDate,
				'ETag': ETag,
				'Expect': List,
				'Expires': HttpDate,
				'From': Str,
				'Host': Str_i,
				'If-Match': ETagList,
				'If-Modified-Since': HttpDate,
				'If-None-Match': ETagList,
				'Last-Modified': HttpDate,
				'Location': Uri,
				'Max-Forwards': Int,
				'Pragma': Dict,
				'Proxy-Authenticate': Challenge,
				'Proxy-Authorization': Credentials,
				'Range': Range,
				'Referer': Uri,
				'Retry-After': HttpDateorInt,
				'Server': Str,
				'Set-Cookie': SetCookie,
				'Set-Cookie2': SemiDictList,
				'TE': QValList,
				'Trailer': HeaderList,
				'Transfer-Encoding': List_i,
				'Upgrade': List,
				'User-Agent': Str,
				'Vary': HeaderList,
				'Via': List,
				'Warning': List,
				'WWW-Authenticate': Challenge,
				}



header_name_cache = {}			# header name lookup cache, no gc
header_name_cache_size = 1000	# how large to grow the cache
header_name_list = map(intern, header_names.keys())
header_name_lower_list = map(lower, header_name_list)

def get_header_name(query):
	'''
	Given a header in any case, return its properly capitalised version.
	'''
	global header_name_cache
	
	if not header_name_cache.has_key(query):
		if len(header_name_cache) > header_name_cache_size:
			header_name_cache = {}
		try:
			header_name_cache[query] = header_name_list \
			  [header_name_lower_list.index(lower(query))]
		except (KeyError, ValueError):
			header_name_cache[query] = capitalize(lower(query))
	return header_name_cache[query]




### Utility Functions


def timegm(tmtuple):
	''' returns epoch seconds from a GMT time tuple. '''
	import calendar
	EPOCH = 1970
	year, month, day, hour, minute, second = tmtuple[:6]
	if year < EPOCH:
		if year < 69:
			year = year + 2000
		else:
			year = year + 1900
		if year < EPOCH:
			raise ValueError, 'invalid year'
	if not 1 <= month <= 12:
		raise TypeError, 'invalid month'
	days = 365 * (year-EPOCH) + calendar.leapdays(EPOCH, year)
	for i in range(1, month):
		days = days + calendar.mdays[i]
	if month > 2 and calendar.isleap(year):
		days = days + 1
	days = days + day - 1
	hours = days * 24 + hour
	minutes = hours * 60 + minute
	seconds = minutes * 60 + second
	return seconds
		

def quotestring(instr, force=0):
	''' does NOT quote control characters. '''
	if not force and \
	  '"' not in instr and \
	  ',' not in instr and \
	  '\\' not in instr and \
	  ';' not in instr:
			return instr
	if instr == '*':
			return instr
	instr = re.sub(r'\\', r'\\\\', instr)
	return '"%s"' % (re.sub(r'"', r'\\"', instr))


def unquotestring(instr):
	''' does NOT unquote control characters. '''
	instr = strip(instr)
	if not instr or instr == '*':
		return instr
	if instr[0] == instr[-1] == '"':
		instr = instr[1:-1]
		instr = re.sub(r'\\(.)', r'\1', instr)
	return instr


