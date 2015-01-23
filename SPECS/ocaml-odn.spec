# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-odn}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:		%{?scl_prefix}ocaml-odn
Version:	0.0.11
Release:	2%{?dist}
Summary:	Dump OCaml data structures using OCaml data notation

License:	LGPL
URL:		https://forge.ocamlcore.org/projects/odn/
Source0:	https://forge.ocamlcore.org/frs/download.php/1310/ocaml-data-notation-%{version}.tar.gz

BuildRequires:	%{?scl_prefix}ocaml >= 3.10.2
BuildRequires:	%{?scl_prefix}ocaml-findlib
BuildRequires:	%{?scl_prefix}ocaml-camlp4-devel
BuildRequires:	%{?scl_prefix}ocaml-type-conv >= 108.07.01
BuildRequires:	%{?scl_prefix}ocaml-ounit-devel >= 2.0.0
BuildRequires:	%{?scl_prefix}ocaml-fileutils-devel >= 0.4.0

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
This library uses type-conv to dump OCaml data structure using OCaml data
notation. This kind of data dumping helps to write OCaml code generator,
like OASIS.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:	%{?scl_prefix}ocaml-type-conv%{_isa} >= 108.07.01

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocaml-data-notation-%{version}

%build
%{?scl:scl enable %{scl} "}
./configure
make
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p \$OCAMLFIND_DESTDIR
make install
%{?scl:"}

%files
%doc CHANGES.txt
%doc COPYING.txt
%{_libdir}/ocaml/odn
%exclude %{_libdir}/ocaml/odn/*.a
%exclude %{_libdir}/ocaml/odn/*.cmxa
%exclude %{_libdir}/ocaml/odn/*.cmx

%files devel
%{_libdir}/ocaml/odn/*.a
%{_libdir}/ocaml/odn/*.cmx
%{_libdir}/ocaml/odn/*.cmxa

%changelog
* Tue Dec 2 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.0.11-2
- SCLify

* Tue Mar 25 2014 Euan Harris <euan.harris@citrix.com> - 0.0.11-1
- Initial package

