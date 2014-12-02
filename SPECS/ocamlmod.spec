%global scl jonludlam-ocaml4021
%{?scl:%scl_package ocamlmod}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} /usr/lib/rpm/ocaml-find-requires.sh -c
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:		%{?scl_prefix}ocamlmod
Version:	0.0.7
Release:	2%{?dist}
Summary:	Generate OCaml modules from source files
License:	LGPL
URL:		http://forge.ocamlcore.org/projects/ocamlmod/
Source0:	http://forge.ocamlcore.org/frs/download.php/1350/%{pkg_name}-%{version}.tar.gz

BuildRequires:	%{?scl_prefix}ocaml >= 3.10.2
BuildRequires:	%{?scl_prefix}ocaml-findlib-devel
BuildRequires:	%{?scl_prefix}ocaml-ounit-devel >= 2.0.0

%description
Generate OCaml modules from source files.

%prep
%setup -q -n %{pkg_name}-%{version}

%build
%{?scl:scl enable %{scl} "}
./configure --prefix %{_prefix} --destdir %{buildroot}
make
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%doc AUTHORS.txt 
%doc CHANGES.txt
%{_bindir}/ocamlmod

%changelog
* Mon Dec 1 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.0.7-2
- SCLify

* Tue Mar 25 2014 Euan Harris <euan.harris@citrix.com> - 0.0.7-1
- Initial package

