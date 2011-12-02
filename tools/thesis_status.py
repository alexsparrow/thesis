#!/usr/bin/env python2
import subprocess, os, sys, getpass
from datetime import datetime

my_path = os.path.join(os.getcwd(), __file__)
base_path = os.path.dirname(my_path)
tex_count_path = os.path.join(base_path, "texcount.pl")


template = r"""
\clearpage
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
\subsection*{Modified (not Committed)}
{\scriptsize
\begin{verbatim}
%(localmods)s
\end{verbatim}
}
\subsection*{Last Commit}
{\scriptsize
\begin{verbatim}
%(lastcommit)s
\end{verbatim}
}
"""

def hostuser():
    return (getpass.getuser(), os.uname()[1])

def ordinal(n):
    m = {1:"st", 2:"nd", 3:"rd"}
    return "%d%s" % (n, m[(n % 10)] if (n%10) in m else "th")
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
def git_last_commit(path):
    return subprocess.check_output(["git", "log", "-1"])

def word_count(path):
    out = subprocess.check_output([tex_count_path, "-inc", "-total", "-q", path])
    results = {}
    for l in out.splitlines():
        if ":" in l: results[l.split(":")[0].strip().rstrip()] = l.split(":")[1].strip().rstrip()
    return results

if __name__ == "__main__":
    target = sys.argv[2]
    head = git_head(os.getcwd())
    wc = word_count(sys.argv[1])
    fields = {
        "user" : hostuser()[0],
        "path" : os.getcwd(),
        "host" : hostuser()[1],
        "built": date(),
        "head": head,
        "wordcount":wc["Words in text"],
        "wordsinheaders" : wc["Words in headers"],
        "wordsincaptions" : wc["Words in float captions"],
        "nheaders" : wc["Number of headers"],
        "nfloats" : wc["Number of floats"],
        "nmathinlines" : wc["Number of math inlines"],
        "nmathdisplays" : wc["Number of math displayed"],
        "localmods": "\n".join(git_local_mods(os.getcwd())),
        "lastcommit": git_last_commit(os.getcwd()),
        "filecount":wc["Files"]}
    open(target, "w").write(template % fields)
