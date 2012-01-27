%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname sqlite3
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')}

Summary:        Allows Ruby scripts to interface with a SQLite3 database
Name:           rubygem-%{gemname}
Version:        1.3.5
Release:        1
Group:          Development/Ruby
License:        BSD
URL:            http://sqlite-ruby.rubyforge.org/
Source0:        http://rubygems.org/gems/%{gemname}-%{version}.gem
Patch0:         %{name}-1.3.3-big-endian.patch
Requires:       rubygems
Requires:       ruby(abi) = 1.8
BuildRequires:  ruby-RubyGems
BuildRequires:  ruby-devel
BuildRequires:  sqlite-devel
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  rubygem(rake)
Obsoletes:      rubygem-sqlite3-ruby < 1.3.3
Provides:       rubygem(%{gemname}) = %{version}-%{release}

%description
SQLite3/Ruby is a module to allow Ruby scripts to interface with a SQLite3
database.

%package        -n ruby-sqlite3
Summary:        A Ruby interface for the SQLite database engine
Group:          Development/Ruby
Requires:       %{name} = %{version}-%{release}
Provides:       ruby(sqlite3) = %{version}-%{release}

%description    -n ruby-sqlite3
Database driver to access SQLite v.3 databases from Ruby.

%package doc
Summary: Documentation for %{name}
Group: Development/Ruby
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -c -T

%build
mkdir -p ./%{gemdir}
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install \
        --local \
        --install-dir ./%{gemdir} \
        -V --force \
        %{SOURCE0}

# Permission
find . -name \*.rb -or -name \*.gem | xargs chmod 0644

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

install -d -m0755 %{buildroot}%{ruby_sitearch}/sqlite3
mv %{buildroot}%{geminstdir}/lib/sqlite3/sqlite3_native.so %{buildroot}%{ruby_sitearch}/sqlite3
rm -rf %{buildroot}%{geminstdir}/ext/

rm -rf %{buildroot}/usr/lib/ruby/gems/1.8/gems/sqlite3-%{version}/.gemtest

# The following method is completely copied from rubygem-gettext
# spec file
#
# Create symlinks
##
## Note that before switching to gem %%{ruby_sitelib}/sqlite3
## already existed as a directory, so this cannot be replaced
## by symlink (cpio fails)
## Similarly, all directories under %%{ruby_sitelib} cannot be
## replaced by symlink
#

create_symlink_rec(){

ORIGBASEDIR=$1
TARGETBASEDIR=$2

## First calculate relative path of ORIGBASEDIR 
## from TARGETBASEDIR
TMPDIR=$TARGETBASEDIR
BACKDIR=
DOWNDIR=
num=0
nnum=0
while true
do
        num=$((num+1))
        TMPDIR=$(echo $TMPDIR | sed -e 's|/[^/][^/]*$||')
        DOWNDIR=$(echo $ORIGBASEDIR | sed -e "s|^$TMPDIR||")
        if [ x$DOWNDIR != x$ORIGBASEDIR ]
        then
                nnum=0
                while [ $nnum -lt $num ]
                do
                        BACKDIR="../$BACKDIR"
                        nnum=$((nnum+1))
                done
                break
        fi
done

RELBASEDIR=$( echo $BACKDIR/$DOWNDIR | sed -e 's|//*|/|g' )

## Next actually create symlink
pushd %{buildroot}/$ORIGBASEDIR
find . -type f | while read f
do
        DIRNAME=$(dirname $f)
        BACK2DIR=$(echo $DIRNAME | sed -e 's|/[^/][^/]*|/..|g')
        mkdir -p %{buildroot}${TARGETBASEDIR}/$DIRNAME
        LNNAME=$(echo $BACK2DIR/$RELBASEDIR/$f | \
                sed -e 's|^\./||' | sed -e 's|//|/|g' | \
                sed -e 's|/\./|/|' )
        ln -s -f $LNNAME %{buildroot}${TARGETBASEDIR}/$f
done
popd

}

create_symlink_rec %{geminstdir}/lib %{ruby_sitelib}

%check
pushd %{buildroot}%{geminstdir}

# fix tests for big endian arches
%ifarch %{sparc} ppc ppc64 s390 s390x
patch -l -p0 < %{PATCH0}
%endif
RUBYOPT="I%{buildroot}%{ruby_sitearch} Ilib" testrb test/test_*

%files
%{ruby_sitearch}/sqlite3

%dir %{geminstdir}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/LICENSE
%{geminstdir}/lib/
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files -n ruby-sqlite3
%{ruby_sitelib}/sqlite3.rb
%{ruby_sitelib}/sqlite3/

%files doc
%doc %{geminstdir}/API_CHANGES.rdoc
%doc %{geminstdir}/CHANGELOG.rdoc
%doc %{geminstdir}/ChangeLog.cvs
%doc %{geminstdir}/Manifest.txt
%{geminstdir}/Rakefile
%{geminstdir}/setup.rb
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/faq/
%{geminstdir}/tasks/
%{geminstdir}/test/
