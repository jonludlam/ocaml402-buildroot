# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-ounit}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}ocaml-ssl
Version:        0.4.7
Release:        2%{?dist}
Summary:        Use OpenSSL from OCaml
License:        LGPL
URL:            http://downloads.sourceforge.net/project/savonet/ocaml-ssl
Source0:        https://github.com/savonet/ocaml-ssl/archive/%{version}/ocaml-ssl-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  openssl-devel

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
Use OpenSSL from OCaml.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocaml-ssl-%{version}

%build
%{?scl:scl enable %{scl} "}
./bootstrap
./configure
make
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
mkdir -p $OCAMLFIND_DESTDIR/stublibs
export OCAMLFIND_LDCONF=ignore
%{?scl:scl enable %{scl} "}
make install DESTDIR=%{buildroot}
%{?scl:"}

%files
%doc CHANGES
%doc COPYING
%doc README
%{_libdir}/ocaml/ssl
%exclude %{_libdir}/ocaml/ssl/*.a
%exclude %{_libdir}/ocaml/ssl/*.cmxa
%exclude %{_libdir}/ocaml/ssl/*.cmx
%exclude %{_libdir}/ocaml/ssl/*.mli
%{_libdir}/ocaml/stublibs/dllssl_stubs.so
%{_libdir}/ocaml/stublibs/dllssl_stubs.so.owner
%{_libdir}/ocaml/stublibs/dllssl_threads_stubs.so
%{_libdir}/ocaml/stublibs/dllssl_threads_stubs.so.owner

%files devel
%{_libdir}/ocaml/ssl/*.a
%{_libdir}/ocaml/ssl/*.cmx
%{_libdir}/ocaml/ssl/*.cmxa
%{_libdir}/ocaml/ssl/*.mli

%changelog
* Sat Dec 6 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.4.7-2
- SCLify

* Thu Oct 2 2014 Euan Harris <euan.harris@citrix.com> - 0.4.7-1
- Update to 0.4.7 and get source from GitHub

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 0.4.6-2
- Split files correctly between base and devel packages

* Sun Jun  2 2013 David Scott <dave.scott@eu.citrix.com> - 0.4.6-1
- Initial package

