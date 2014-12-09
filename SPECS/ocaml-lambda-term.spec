# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml4021 in this case
%global scl ocaml4021
%endif

%{?scl:%scl_package ocaml-lambda-term}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}ocaml-lambda-term
Version:        1.6
Release:        2%{?dist}
Summary:        Lambda-Term is a cross-platform library for manipulating the terminal for Ocaml
License:        BSD3
URL:            http://forge.ocamlcore.org/projects/lambda-term/
Source0:        https://github.com/diml/lambda-term/archive/%{version}/lambda-term-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-camomile-devel
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-lwt-devel
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-react-devel
BuildRequires:  %{?scl_prefix}ocaml-zed-devel

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
Lambda-Term is a cross-platform library for manipulating the terminal.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}ocaml-lwt-devel%{?_isa}
Requires:       %{?scl_prefix}ocaml-zed-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n lambda-term-%{version}

%build
%{?scl:scl enable %{scl} "}
./configure --destdir %{buildroot}/%{_libdir}/ocaml
make
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
mkdir -p $OCAMLFIND_DESTDIR/stublibs
export OCAMLFIND_LDCONF=ignore
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

rm -f %{buildroot}/%{_libdir}/ocaml/usr/local/bin/lambda-term-actions

%files
%doc CHANGES.md
%doc LICENSE
%{_libdir}/ocaml/lambda-term
%{_libdir}/ocaml/stublibs/dlllambda-term_stubs.so
%{_libdir}/ocaml/stublibs/dlllambda-term_stubs.so.owner
%exclude %{_libdir}/ocaml/lambda-term/*.a
%exclude %{_libdir}/ocaml/lambda-term/*.cmxa
%exclude %{_libdir}/ocaml/lambda-term/*.cmx
%exclude %{_libdir}/ocaml/lambda-term/*.mli

%files devel
%{_libdir}/ocaml/lambda-term/*.a
%{_libdir}/ocaml/lambda-term/*.cmx
%{_libdir}/ocaml/lambda-term/*.cmxa
%{_libdir}/ocaml/lambda-term/*.mli

%files devel
%{_libdir}/ocaml/lambda-term/*.a
%{_libdir}/ocaml/lambda-term/*.cmx
%{_libdir}/ocaml/lambda-term/*.cmxa
%{_libdir}/ocaml/lambda-term/*.mli

%changelog
* Tue Dec 9 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.6-2
- SCLify

* Sat Jun  7 2014 David Scott <dave.scott@citrix.com> - 1.6-1
- Update to 1.6

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 1.2-2
- Split files correctly between base and devel packages

* Thu Jun  6 2013 David Scott <dave.scott@eu.citrix.com> - 1.2-1
- Initial package

