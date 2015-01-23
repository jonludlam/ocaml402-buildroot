# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package cppo}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}cppo
Version:        1.1.2
Release:        1%{?dist}
Summary:        Equivalent of the C preprocessor for OCaml
License:        BSD3
URL:            http://mjambon.com/cppo.html
Source0:        https://github.com/mjambon/cppo/archive/v%{version}/cppo-%{version}.tar.gz

BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
Equivalent of the C preprocessor for OCaml.

%prep
%setup -q -n %{pkg_name}-%{version}

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
mkdir -p %{buildroot}/%{_bindir}
%{?scl:scl enable %{scl} "}
make install BINDIR=%{buildroot}/%{_bindir}
%{?scl:"}

%files
%doc LICENSE 
%doc README.md
%{_bindir}/cppo
%{_libdir}/ocaml/cppo_ocamlbuild

%changelog
* Tue Dec 9 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.1.2-1
- New version

* Mon Dec 1 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.3-3
- SCLify

* Tue Oct 21 2014 Euan Harris <euan.harris@citrix.com> - 0.9.3-2
- Switch to GitHub sources

* Fri May 31 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.3-1
- Initial package

