%define name pyPgSQL
%define version 2.4
%define release %mkrel 4

#  automatically set GCC flags based on version
%define cflags -std=c99 %optflags

Summary: pyPgSQL - A Python DB-API 2.0 compliant interface to PostgreSQL
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://telia.dl.sourceforge.net/sourceforge/pypgsql/%name-%{version}.tar.bz2
Patch: pypgsql-2.3-mdk.patch.bz2
License: BSD
Group: Development/Python
BuildRoot: %{_tmppath}/%{name}-buildroot
Url: http://pypgsql.sourceforge.net/
Requires: egenix-mx-base , python >= 2.2 , postgresql
BuildRequires: python-devel , postgresql-devel

%description
pyPgSQL is a package of two modules that provide a Python DB-API 2.0
compliant interface to PostgreSQL databases. The first module, libpq,
exports the PostgreSQL C API to Python. This module is written in C and
can be compiled into Python or can be dynamically loaded on demand. The
second module, PgSQL, provides the DB-API 2.0 compliant interface and
support for various PostgreSQL data types, such as INT8, NUMERIC, MONEY,
BOOL, ARRAYS, etc. This module is written in Python.

%prep
%setup -q -n pypgsql

%patch -p1

%build
env CFLAGS="%{cflags}" /usr/bin/python setup.py build

#  change the path in the test/examples
find test examples -type f | while read file
do
   echo "Fixing path in $file"
   sed -i 's|^#!.*|#!/usr/bin/env python|' $file
done

%install
# remove CVS files
find . -type d -name CVS | xargs rm -rf

%_bindir/python setup.py install --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc README Announce ChangeLog
%doc examples test
%_libdir/python%pyver/site-packages/%{name}
%_libdir/python%pyver/site-packages/*-info
