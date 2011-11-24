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

%% My additions
%% Import package
\RequirePackage{import}
\RequirePackage{lineno}
\RequirePackage[nolist]{acronym}
\RequirePackage{ctable}

% TODO notes in the margin
%\RequirePackage{todonotes}

% These are apparently needed to stop microtype from bitching
% http://www.freak-search.com/en/thread/888630/microtype_and_siunitx_micro_unsupported
% They seem to have the side effect of making the DRAFT text much bigger
% \RequirePackage[T1]{fontenc}
% \RequirePackage{microtype,textcomp}

\RequirePackage{thesisdefs}

% I want a tick symbol
\RequirePackage{amsfonts}
