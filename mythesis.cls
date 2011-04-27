\ProvidesClass{thesis}
%% For normal draft builds
\LoadClass[hyperpdf,nobind,draft,sftitles,oneside]{hepthesis}
%\LoadClass[hyperpdf,nobind,draft,twoside]{hepthesis}
%% For short draft builds (breaks citations by necessity)
%\LoadClass[hyperpdf,nobind,draft,hidefrontback]{hepthesis}
%% For Cambridge soft-bound version
%\LoadClass[hyperpdf,bindnopdf]{hepthesis}
%% For Cambridge hard-bound version (must be one-sided)
%\LoadClass[hyperpdf,oneside]{hepthesis}

%% -------------------------------------
%% Standard packages
%% -------------------------------------
\RequirePackage{cite}
%\RequirePackage{morefloats}
\RequirePackage{mathrsfs} % script font
\RequirePackage{afterpage}

%% Using Babel allows other languages to be used and mixed-in easily
\RequirePackage[ngerman,english]{babel}
\selectlanguage{english}

%% Quotes in different languages are different.
%% Using \enquote{bla} automatically uses the correct quotes
%% according to the Babel language that is set
\RequirePackage[babel]{csquotes}

%% Subfigures - note subfig is incompatible with ccaption
\RequirePackage{subfig}

%% TikZ is a marvellous drawing package
\RequirePackage{tikz}
