#!/usr/bin/env python2

from HTMLParser import HTMLParser, HTMLParseError
from xml.sax.saxutils import escape
import cgi_buffer, namegen, paranoia, sys

class ParanoiaParser(HTMLParser, object):
    def __init__(self):
        super(ParanoiaParser, self).__init__()

        self.procs = {}
        self.procs['make-random-char?'] = self.make_random_char

    def handle_starttag(self, tag, attrs):
        s = "<%s" % tag
        for keyval in attrs:
            s += ' %s="%s"' % keyval
        s += ">"
        sys.stdout.write(s)

    def handle_endtag(self, tag):
        sys.stdout.write('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        sys.stdout.write('</%s' % tag)
        for keyval in attrs:
            sys.stdout.write('%s="%s"' % keyval)
        sys.stdout.write('>')

    def handle_pi(self, data):
        try:
            self.procs[data]()
        except KeyError:
            raise HTMLParseError(data)

    def handle_data(self, data):
        sys.stdout.write(data)

    def handle_decl(self, decl):
        sys.stdout.write('<!%s>' % decl)

    def reset_procs(self):
        for key in self.procs.keys():
            del self.procs[key]

    def make_random_char(self):
        self.char = paranoia.make_random_char()

        self.reset_procs()
        self.procs['name?'] = lambda name = namegen.random_name(): sys.stdout.write(name)
        for skill in self.char.skills:
            s = '<table class="skill"><caption>%s</caption>\n' % escape(skill.name.title())
            s += '<tbody class="specs">'
            for spec in skill:
                s += '<tr><td>%s</td><td>%s</td></tr>\n' % (escape(spec.title()), skill[spec])
            s += '</tbody>\n</table>'
            self.procs['skill-table=%s?' % skill.name] = lambda s=s: sys.stdout.write(s)
        self.procs['service-group?'] = lambda: sys.stdout.write(self.expand_group(self.char.group))

    def expand_group(self, group, depth=0):
        s = '<div class="'
        if group.spyfor != None:
            s += 'spy"'
            if group.cover != None:
                s += ' cover="%s" coverfirm="%s">' % (group.cover, group.coverfirm)
            else:
                s += '>'
        else:
            s += 'group">%s' % escape(group.group)
        if group.firm != None:
            s += '<div class="firm">%s</div>' % escape(group.firm)
        if group.spyfor != None:
            s += '<div class="spyfor">%s</div>' % self.expand_group(group.spyfor, depth+1)
            if group.spyon != None:
                s += '<div class="spyon">%s</div>' % self.expand_group(group.spyon, depth+1)
        s += '</div>'
        return s


if __name__ == '__main__':
    print 'Content-Type: text/html; charset=iso-8859-1'
    print
    parser = ParanoiaParser()
    parser.feed(open('paranoia-template.xml').read())