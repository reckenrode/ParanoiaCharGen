import random
import linecache
import string

# inspired by http://mail.python.org/pipermail/tutor/2001-December/010650.html

def count_lines(file):
    """Given a file, returns the number of lines it contains.
    The current file position should be preserved as long as the file
    supports tell() and seek()."""
    old_position = file.tell()
    file.seek(0)
    count = 0
    while file.readline() != '':
        count += 1
    file.seek(old_position)
    return count

def random_line(filename):
    """Given a filename, returns a random line."""
    linecount = count_lines(open(filename))
    chosen_line_number = random.randrange(linecount)
    return linecache.getline(filename, chosen_line_number)

def random_char():
    return random.choice(string.ascii_uppercase)

def random_name():
    namefile = random.choice(["female-names", "male-names"])
    firstname = random_line(namefile).strip()
    sector = ""
    for i in xrange(3):
        sector += random_char()
    return "%s-%s-%s-%i" % (firstname, 'R', sector, 1)

if __name__ == "__main__":
    print random_name()
