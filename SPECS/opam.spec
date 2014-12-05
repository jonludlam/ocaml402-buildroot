# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml4021 in this case
%global scl ocaml4021
%endif

%{?scl:%scl_package opam}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}opam
Version:        1.1.2
Release:        2%{?dist}
Summary:        Source-based OCaml package manager
License:        LGPLv3
URL:            http://opam.ocaml.org/
Source0:        https://github.com/ocaml/opam/releases/download/%{version}/opam-full-%{version}.tar.gz
BuildRequires:  curl 
BuildRequires:  %{?scl_prefix}ocaml 

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
Source-based OCaml package manager

%prep
%setup -q -n opam-full-%{version}

%build
%{?scl:scl enable %scl - << \EOF}
%configure
make lib-ext
make
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} "}
make install DESTDIR=%{buildroot}
%{?scl:"}
mkdir -p %{buildroot}/%{_mandir}
mv %{buildroot}%{?_scl_root}/usr/man/* %{buildroot}/%{_mandir}
rm -rf %{buildroot}%{?_scl_root}/usr/man

%files
%doc AUTHORS
%doc CHANGES
%doc CONTRIBUTING.md
%doc LICENSE
%doc README.md
%{_mandir}/man1/opam*
%{_bindir}/opam
%{_bindir}/opam-admin
%{_bindir}/opam-installer

%changelog
* Thu Dec 04 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.1.2-2
- SCLify

* Fri Aug 01 2014 Euan Harris <euan.harris@citrix.com> - 1.1.2-1
- Initial package

