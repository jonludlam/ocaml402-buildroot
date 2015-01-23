# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-ocplib-endian}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}ocaml-ocplib-endian
Version:        0.4
Release:        3%{?dist}
Summary:        Optimized functions to read and write int16/32/64 from strings and bigarrays
License:        LGPL
URL:            https://github.com/OCamlPro/ocplib-endian
Source0:        https://github.com/OCamlPro/ocplib-endian/archive/%{version}/ocplib-endian-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}optcomp

%description
Optimised functions to read and write int16/32/64 from strings and
bigarrays, based on new primitives added in version 4.01.

The library implements two modules:
- [EndianString](ocplib-endian/blob/master/src/endianString.mli) works
  directly on strings, and provides submodules BigEndian and LittleEndian,
  with their unsafe counter-parts;

- [EndianBigstring](ocplib-endian/blob/master/src/endianBigstring.mli)
  works on bigstrings (Bigarrays of chars), and provides submodules
  BigEndian and LittleEndian, with their unsafe counter-parts;


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       optcomp

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocplib-endian-%{version}

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure
ocaml setup.ml -build
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
ocaml setup.ml -install
%{?scl:"}

%files
%doc COPYING.txt
%doc README.md
%{_libdir}/ocaml/ocplib-endian
%exclude %{_libdir}/ocaml/ocplib-endian/*.a
%exclude %{_libdir}/ocaml/ocplib-endian/*.cmxa
%exclude %{_libdir}/ocaml/ocplib-endian/*.cmx
%exclude %{_libdir}/ocaml/ocplib-endian/*.mli

%files devel
%{_libdir}/ocaml/ocplib-endian/*.a
%{_libdir}/ocaml/ocplib-endian/*.cmx
%{_libdir}/ocaml/ocplib-endian/*.cmxa
%{_libdir}/ocaml/ocplib-endian/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.4-3
- SCLify

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 0.4-2
- Split files correctly between base and devel packages

* Fri May 31 2013 David Scott <dave.scott@eu.citrix.com> - 0.4-1
- Initial package

