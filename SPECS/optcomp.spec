# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package optcomp}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}optcomp
Version:        1.6
Release:        1%{?dist}
Summary:        Optional compilation with cpp-like directives
License:        BSD3
URL:            https://github.com/diml/optcomp
Source0:        https://github.com/diml/optcomp/archive/%{version}/optcomp-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc

%description
Optional compilation with cpp-like directives.

%prep
%setup -q -n optcomp-%{version}

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure --destdir %{buildroot}/%{_libdir}/ocaml
ocaml setup.ml -build
%{?scl:"}

%install
mkdir -p %{buildroot}/%{_libdir}/ocaml
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
%{?scl:scl enable %{scl} "}
ocaml setup.ml -install
%{?scl:"}
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}/%{_libdir}/ocaml/usr/local/bin/optcomp-r %{buildroot}/%{_bindir}/
mv %{buildroot}/%{_libdir}/ocaml/usr/local/bin/optcomp-o %{buildroot}/%{_bindir}/


%files
%doc LICENSE
%doc README.md
%{_libdir}/ocaml/optcomp
%{_bindir}/optcomp-r
%{_bindir}/optcomp-o

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.6-2
- SCLify

* Thu Oct 2 2014 Euan Harris <euan.harris@citrix.com> - 1.6-1
- Update to 1.6 and switch to GitHub sources

* Fri May 31 2013 David Scott <dave.scott@eu.citrix.com> - 1.4-1
- Initial package

