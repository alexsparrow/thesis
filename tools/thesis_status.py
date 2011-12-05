#!/usr/bin/env python2
import subprocess, os, sys, getpass
from datetime import datetime

my_path = os.path.join(os.getcwd(), __file__)
base_path = os.path.dirname(my_path)
tex_count_path = os.path.join(base_path, "texcount.pl")


template = r"""
\clearpage
%(verbs)s
\section*{Status}
Built by \textbf{%(user)s} on host \textbf{%(host)s} at \textbf{%(built)s}. \\
Path is \verb|%(path)s|

\ctable[
cap=Thesis Status,
caption=Thesis Status,
mincapwidth=\textwidth,
pos=h
]{ll}{}{\FL
Revision  & %(head)s \ML
Words in Text & %(wordcount)s \NN
Words in Headers & %(wordsinheaders)s \NN
Words in Captions & %(wordsincaptions)s \ML
Number of Headers & %(nheaders)s \NN
Number of Floats & %(nfloats)s \NN
Number of Math Inlines & %(nmathinlines)s \NN
Number of Math Displays & %(nmathdisplays)s \ML
Files & %(filecount)s \LL
}

\ctable[
cap=Thesis Files,
caption=Thesis Files,
mincapwidth=\textwidth,
pos=h,
doinside=\scriptsize
]{llll}{}{\FL
File & Words in Text & Words in Headers & Words in Captions \ML
%(file_table)s
}

\subsection*{Modified (not Committed)}
{\scriptsize
\begin{verbatim}
%(localmods)s
\end{verbatim}
}
\subsection*{Recent Commits}
{\scriptsize
\begin{verbatim}
%(lastcommit)s
\end{verbatim}
}
"""

file_row_template=r"\UseVerb{%(name)s} & %(wordcount)d & %(wordsinheaders)d & %(wordsincaptions)d %(endline)s"

def hostuser():
    return (getpass.getuser(), os.uname()[1])

def ordinal(n):
    m = {1:"st", 2:"nd", 3:"rd"}
    if (n % 10) in m: ords = m[(n % 10)]
    else ords = "th"
    return "%d%s" % (n, ords)

def date():
    dt = datetime.now()
    return dt.strftime("%H:%M, %A "+ ordinal(dt.day) +" %B, %Y")

def git_head(path):
    return subprocess.check_output(["git", "rev-parse", "HEAD"])
def git_local_mods(path):
    out = subprocess.check_output(["git", "status", "--porcelain"])
    modf = []
    for l in out.splitlines():
        if l.strip()[0] == "M": modf.append(l.split()[-1])
    return modf
def git_last_commit(path, n):
    return subprocess.check_output(["git", "log", "-%d" % n])

def word_count(path):
    out = subprocess.check_output([tex_count_path, "-inc", "-q", path])
    results = {}
    name = None
    for l in out.splitlines():
        if not ":" in l: continue
        k, v = l.split(":")[0].strip().rstrip(), l.split(":")[1].strip().rstrip()
        if k in ["File", "Included file"]:
            name = v
            results[name] = {}
        elif k == "File(s) total":
            name = "total"
            results[name] = {}
        elif name is not None: results[name][k] = v
    return results

def extract_wordcount(d):
    fields = [
        ("wordcount", "Words in text"),
        ("wordsinheaders" ,"Words in headers"),
        ("wordsincaptions" ,"Words in float captions"),
        ("nheaders" ,"Number of headers"),
        ("nfloats" ,"Number of floats"),
        ("nmathinlines" ,"Number of math inlines"),
        ("nmathdisplays" ,"Number of math displayed"),
        ("filecount", "Files")
        ]
    out = {}
    for x, y in fields:
        try: out[x] = int(d[y])
        except: out[x] = -1
    return out

if __name__ == "__main__":
    fname = sys.argv[1]
    head = git_head(os.getcwd())
    wc = word_count(fname)

    verbs = []
    file_table = ""
    files = [k for k in wc.keys() if k!= "total"]
    for idx, n in enumerate(sorted(files)):
        wc_file = extract_wordcount(wc[n])
        subs = wc_file.copy()
        verbs.append(r"\SaveVerb{v%d}|%s|" % (idx, n))
        subs["name"] = "v%d" % idx
        subs["endline"] = "\\NN\n" if idx != len(files)-1 else r"\LL"
        file_table += file_row_template % subs

    fields = {
        "verbs" : "\n".join(verbs),
        "user" : hostuser()[0],
        "path" : os.getcwd(),
        "host" : hostuser()[1],
        "built": date(),
        "head": head,
        "localmods": "\n".join(git_local_mods(os.getcwd())),
        "lastcommit": git_last_commit(os.getcwd(), 5),
        "file_table": file_table
        }
    fields.update(extract_wordcount(wc["total"]))
    print template % fields
