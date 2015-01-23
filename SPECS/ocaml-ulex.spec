# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-jsonm}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}ocaml-ulex
Version:        1.1
Release:        2%{?dist}
Summary:        lexer generator for Unicode and OCaml
License:        ISC
URL:            http://ftp.de.debian.org/debian/pool/main/u/ulex/ulex_1.1.orig.tar.gz
Source0:        http://ftp.de.debian.org/debian/pool/main/u/ulex/ulex_1.1.orig.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel

%description
lexer generator for Unicode and OCaml

%prep
%setup -q -n ulex-%{version}

%build
%{?scl:scl enable %{scl} "}
make
make all.opt
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%{_libdir}/ocaml/ulex
%{_libdir}/ocaml/ulex/*.a
%{_libdir}/ocaml/ulex/*.cmxa
%{_libdir}/ocaml/ulex/*.cmx
%{_libdir}/ocaml/ulex/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.1-2
- SCLify

* Thu Oct 16 2014 David Scott <dave.scott@citrix.com> - 1.1-1
- Initial package
