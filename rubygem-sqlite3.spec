%define	rbname	sqlite3

Summary:	Interface with the SQLite3 database engine
Name:		rubygem-%{rbname}

Version:	1.3.9
Release:	1
Group:		Development/Ruby
License:	GPLv2+ or Ruby
URL:		http://github.com/luislavena/sqlite3-ruby
Source0:	http://gems.rubyforge.org/gems/%{rbname}-%{version}.gem
BuildRequires:	rubygems >= 1.3.5
BuildRequires:	ruby-devel
BuildRequires:	rubygem(rake)
BuildRequires:  sqlite-devel
BuildRequires:  pkgconfig(sqlite3)


%description
This module allows Ruby programs to interface with the SQLite3
database engine (http://www.sqlite.org).  You must have the
SQLite engine installed in order to build this module.
Note that this module is only compatible with SQLite 3.6.16 or newer.

%files
%{ruby_gemdir}/gems/%{rbname}-%{version}/lib/*.rb
%{ruby_gemdir}/gems/%{rbname}-%{version}/lib/sqlite3/*.rb
%{ruby_gemdir}/specifications/%{rbname}-%{version}.gemspec
%{ruby_sitearchdir}/%{rbname}/*.so

#--------------------------------------------------------
%package	doc
Summary:	Documentation for %{name}
Group:		Books/Computer books
Requires:	%{name} = %{EVRD}
BuildArch:	noarch

%description	doc
Documents, RDoc & RI documentation for %{name}.

%files doc
%doc %{ruby_gemdir}/gems/%{rbname}-%{version}/*.rdoc
%doc %{ruby_gemdir}/gems/%{rbname}-%{version}/*.txt
%doc %{ruby_gemdir}/gems/%{rbname}-%{version}/ext/sqlite3/*.c
%doc %{ruby_gemdir}/doc/%{rbname}-%{version}
#--------------------------------------------------------

%prep
%setup -q

%build
%gem_build

%install
%gem_install






