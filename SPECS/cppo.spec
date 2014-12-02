%global scl jonludlam-ocaml4021
%{?scl:%scl_package cppo}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} /usr/lib/rpm/ocaml-find-requires.sh -c
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}cppo
Version:        0.9.3
Release:        3%{?dist}
Summary:        Equivalent of the C preprocessor for OCaml
License:        BSD3
URL:            http://mjambon.com/cppo.html
Source0:        https://github.com/mjambon/%{pkg_name}/archive/v%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  %{?scl_prefix}ocaml

%description
Equivalent of the C preprocessor for OCaml.

%prep
%setup -q -n %{pkg_name}-%{version}

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}


%install
mkdir -p %{buildroot}/%{_bindir}
make install BINDIR=%{buildroot}/%{_bindir}

%files
%doc LICENSE 
%doc README
%{_bindir}/cppo

%changelog
* Mon Dec 1 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.3-3
- SCLify

* Tue Oct 21 2014 Euan Harris <euan.harris@citrix.com> - 0.9.3-2
- Switch to GitHub sources

* Fri May 31 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.3-1
- Initial package

