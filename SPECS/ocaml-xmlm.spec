# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-async-find}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif


Name:           %{?scl_prefix}ocaml-xmlm
Version:        1.2.0
Release:        2%{?dist}
Summary:        Streaming XML input/output for OCaml
License:        BSD
URL:            http://erratique.ch/software/xmlm
Source0:        https://github.com/dbuenzli/xmlm/archive/v%{version}/xmlm-%{version}.tar.gz
Obsoletes:      xmlm <= 1.1.1
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc

%description
Xmlm is an OCaml module providing streaming XML input/output. It aims at
making XML processing robust and painless.

The streaming interface can process documents without building an in-memory
representation. It lets the programmer translate its data structures to
XML documents and vice-versa. Functions are provided to easily transform
arborescent data structures to/from XML documents.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n xmlm-%{version}

%build
%{?scl:scl enable %{scl} "}
./pkg/pkg-git
./pkg/build true
%{?scl:"}

%install
find .
mkdir -p %{buildroot}/%{_libdir}/ocaml/xmlm
cp _build/pkg/META  _build/src/xmlm.a  _build/src/xmlm.cma  _build/src/xmlm.cmi  _build/src/xmlm.cmx  _build/src/xmlm.cmxa  _build/src/xmlm.cmxs  _build/src/xmlm.mli  %{buildroot}/%{_libdir}/ocaml/xmlm



%files
%doc CHANGES.md
%doc README.md
%{_libdir}/ocaml/xmlm
%exclude %{_libdir}/ocaml/xmlm/*.a
%exclude %{_libdir}/ocaml/xmlm/*.cmxa
%exclude %{_libdir}/ocaml/xmlm/*.cmx
%exclude %{_libdir}/ocaml/xmlm/*.mli

%files devel
%{_libdir}/ocaml/xmlm/*.a
%{_libdir}/ocaml/xmlm/*.cmxa
%{_libdir}/ocaml/xmlm/*.cmx
%{_libdir}/ocaml/xmlm/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.2.0-2
- SCLify

* Thu Jul 17 2014 David Scott <dave.scott@citri.com> - 1.2.0-1
- Update to 1.2.0

* Mon Jun 2 2014 Euan Harris <euan.harris@citrix.com> - 1.1.1-3
- Split files correctly between base and devel packages

* Mon May 19 2014 Euan Harris <euan.harris@citrix.com> - 1.1.1-2
- Switch to GitHub mirror

* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com> - 1.1.1-1
- Initial package

