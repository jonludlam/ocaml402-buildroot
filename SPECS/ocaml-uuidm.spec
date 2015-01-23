# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-uuidm}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}ocaml-uuidm
Version:        0.9.5
Release:        4%{?dist}
Summary:        Universally Unique IDentifiers (UUIDs) for OCaml
License:        BSD
URL:            http://erratique.ch/software/uuidm
Source0:        https://github.com/dbuenzli/uuidm/archive/v%{version}/uuidm-%{version}.tar.gz
Patch0:         uuidm.oasis.patch
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc

%description
Uuidm is an OCaml module implementing 128 bits universally unique
identifiers version 3, 5 (named based with MD5, SHA-1 hashing) and 4
(random based) according to RFC 4122.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n uuidm-%{version}
%patch0 -p1

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure --destdir %{buildroot}/%{_libdir}/ocaml
ocaml setup.ml -build
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
ocaml setup.ml -install
%{?scl:"}
rm -f %{buildroot}/%{_libdir}/ocaml/usr/local/bin/uuidtrip

%files
%doc CHANGES
%doc README
%{_libdir}/ocaml/uuidm
%exclude %{_libdir}/ocaml/uuidm/*.a
%exclude %{_libdir}/ocaml/uuidm/*.cmxa
%exclude %{_libdir}/ocaml/uuidm/*.cmx
%exclude %{_libdir}/ocaml/uuidm/*.mli

%files devel
%{_libdir}/ocaml/uuidm/*.a
%{_libdir}/ocaml/uuidm/*.cmx
%{_libdir}/ocaml/uuidm/*.cmxa
%{_libdir}/ocaml/uuidm/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.5-4
- SCLify

* Mon Jun 02 2014 Euan Harris <euan.harris@citrix.com> - 0.9.5-3
- Split files correctly between base and devel packages

* Mon May 19 2014 Euan Harris <euan.harris@citrix.com> - 0.9.5-2
- Switch to GitHub mirror

* Wed May 29 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.5-1
- Initial package

