#!/bin/sh

sudo apt-get install ruby rake texlive-humanities texlive-science
ruby -e "require 'rake-latex'"
if [ $? -eq 1 ] 
then
   wget "http://devel.softeng.ox.ac.uk/download/rake-latex-0.5.4.tar.gz"
   tar -xvzf "rake-latex-0.5.4.tar.gz"
   cd rake-latex-0.5.4
   sudo ruby setup.rb
   cd ..
else
   echo "Rake-LaTeX found. No need to install"
fi
