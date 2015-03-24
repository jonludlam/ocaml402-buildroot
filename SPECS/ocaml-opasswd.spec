# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-opasswd}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocaml-opasswd
Version:        0.9.3
Release:        2%{?dist}
Summary:        OCaml interface to the glibc passwd/shadow password functions
License:        ISC
URL:            https://github.com/xapi-project/ocaml-opasswd
Source0:        https://github.com/xapi-project/ocaml-opasswd/archive/%{version}/ocaml-opasswd-%{version}.tar.gz
Patch0:         ocaml-opasswd-ocaml-4.00.1.patch
BuildRequires:  %{?scl_prefix}ocaml 
BuildRequires:  %{?scl_prefix}ocaml-findlib 
BuildRequires:  %{?scl_prefix}ocaml-ctypes-devel 
BuildRequires:  libffi-devel

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
This is an OCaml binding to the glibc passwd file and shadow password
file interface. It can be used to read, parse, manipulate and write
passwd and shadow files on Linux systems. It might also work on other
nixes, but it has not been tested.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}ocaml-ctypes-devel%{?_isa}
Requires:       %{?scl_prefix}libffi%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocaml-opasswd-%{version}
%patch0 -p1

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure --destdir %{buildroot}%{_libdir}/ocaml
ocaml setup.ml -build
%{?scl:"}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/ocaml
export OCAMLFIND_LDCONF=ignore
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
%{?scl:scl enable %{scl} "}
ocaml setup.ml -install
%{?scl:"}
rm -f %{buildroot}%{_libdir}/ocaml/usr/local/bin/opasswd_test

%files
%doc README.md
%{_libdir}/ocaml/oPasswd
%exclude %{_libdir}/ocaml/oPasswd/*.a
%exclude %{_libdir}/ocaml/oPasswd/*.cmxa
%exclude %{_libdir}/ocaml/oPasswd/*.mli

%files devel
%{_libdir}/ocaml/oPasswd/*.a
%{_libdir}/ocaml/oPasswd/*.cmxa
%{_libdir}/ocaml/oPasswd/*.mli

%changelog
* Mon Mar 23 2015 Jon Ludlam <jonathan.ludlam@citrix.cim> - 0.9.3-2
- SCLify

* Thu May  1 2014 David Scott <dave.scott@citrix.com> - 0.9.3-1
- For -devel package add dependency on ocaml-ctypes-devel

* Thu Apr 24 2014 David Scott <dave.scott@citrix.com>
- Fix split between -devel and main package, hopefully

* Thu Oct 31 2013 Mike McClurg <mike.mcclurg@citrix.com>
- Initial package

