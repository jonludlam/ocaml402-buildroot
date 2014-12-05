# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml4021 in this case
%global scl ocaml4021
%endif

%{?scl:%scl_package ocaml-odn}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}ocaml-obuild
Version:        0.0.2
Release:        2%{?dist}
Summary:        Simple build tool for OCaml programs
License:        BSD2
URL:            https://github.com/vincenthz/obuild
Source0:        https://github.com/vincenthz/obuild/archive/v%{version}/obuild-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
The goal is to make a very simple build system for users and developers 
of OCaml libraries and programs.

Obuild acts as a building black box: user declares only what they want to 
build and with which sources, and the build system will consistently 
build it.

The design is based on cabal, and borrows most of its layout and way of 
working, adapting parts where necessary to support OCaml fully.

%prep
%setup -q -n obuild-%{version}

%build
%{?scl:scl enable %{scl} "}
./bootstrap
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
mkdir -p %{buildroot}/%{_bindir}
install dist/build/obuild/obuild %{buildroot}/%{_bindir}
install dist/build/obuild-simple/obuild-simple %{buildroot}/%{_bindir}
install dist/build/obuild-from-oasis/obuild-from-oasis %{buildroot}/%{_bindir}
%{?scl:"}

%files
%doc README.md TODO.md DESIGN.md LICENSE OBUILD_SPEC.md
%{_bindir}/obuild
%{_bindir}/obuild-simple
%{_bindir}/obuild-from-oasis

%changelog
* Wed Dec 3 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.0.2-2
- SCLify

* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com> - 0.0.2-1
- Initial package

