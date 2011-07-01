require 'rake-latex'

Rake.startfile(__FILE__)

# LaTeX document in mydoc.tex.
latex('thesis')

latex('thesis') do
  |task|
  task.includes = [
    "1-theory/theory.tex",
    "ch2-expt.tex",
    "ch3-wpol.tex",
    "ch4-susy.tex",
    "ch5-interpretation.tex"
  ]
end

Rake.endfile
