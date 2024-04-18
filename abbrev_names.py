# This script will take as an input file references_full.bib and modify it writing the output to references.bib
# It will modify titles to be lower case except for the first word and the special cases listed below.
# It will also abbreviate first names such that Briney, Sam becomes Briney, S.
import bibtexparser as bp

fname_in = 'references_full.bib'
fname_out = 'references.bib'

fin = open(fname_in, 'r')

# build special case table for fixing titles
rep_table_new = ['WENO', 'AUSM', 'AUSM', 'AUSM+', 'Reynolds', 'Rayleigh-Taylor', 'Rayleigh–Taylor', 'Richtmyer–Meshkov', 'Re', 'Euler–Lagrange',  'Euler-Lagrange', 'Euler–Euler', 'Euler-Euler', 'Bell–Plesset', 'Bell-Plesset']
rep_table_old = []
for new in rep_table_new:
    rep_table_old.append(new.lower())

db = bp.load(fin)
for entry in db.entries:
    authors = entry['author'].split(' and ')

    authors_new = []

    # abbreviate names
    for author in authors:
        names = author.split(',')
        for i, name in enumerate(names):
            names[i] = name.strip()

        try:
            fnames = names[1].split()
        except:
            continue

        for i, fname in enumerate(fnames):
            if fname.find('-') == -1:
                if fname[-1] != '.':
                    fnames[i] = fname[0] + '.'
            else:
                fname_sp = fname.split('-')
                for j, fnamej in enumerate(fname_sp):
                    fname_sp[j] = fnamej[0] + '.'

                fnames[i] = '-'.join(fname_sp)

        names[1] = ''.join(fnames)

        # WARNING---------------- be careful here
        #names[0] = names[0].capitalize() # This will be a problem for names like O'Reilly, etc.

        authors_new.append(', '.join(names))

    entry['author'] = ' and '.join(authors_new)

    # lower case titles
    title = entry['title'].replace('{', '').replace('}', '')
    title = title.lower().capitalize()

    words = title.split(' ')

    p = False
    for i, word in enumerate(words):
        if word[-1] == '.' or word[-1] == ':':
            w = word[:-1]
            add = word[-1]
        else:
            add = ''
            w = word

        if w.lower() in rep_table_old:
            words[i] = rep_table_new[rep_table_old.index(w.lower())] + add
            p = True

    for i in range(1, len(words)):
        word = words[i]
        if words[i-1][-1] == '.':
            words[i] = word.capitalize()

    title = ' '.join(words)

    entry['title'] = '{' + title + '}'

    if p:
        print(title)


fin.close()

fout = open(fname_out, 'w')
bp.dump(db, fout)
fout.close()

