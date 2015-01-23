# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package utop}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}utop
Version:        1.16
Release:        1%{?dist}
Summary:        A toplevel for OCaml which can run in a terminal or in Emacs
License:        BSD
URL:            https://github.com/diml/utop
Source0:        https://github.com/diml/utop/archive/%{version}/utop-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-lambda-term-devel
BuildRequires:  %{?scl_prefix}cppo

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Requires: %{?scl_prefix}ocaml-camomile-data

%description
utop is a toplevel for OCaml which can run in a terminal or in Emacs. It
supports completion, colors, parenthesis matching, ...

%prep
%setup -q -n utop-%{version}

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure --prefix %{_prefix} --destdir %{buildroot}
ocaml setup.ml -build
%{?scl:"}

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_libdir}/ocaml
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
export OCAMLFIND_LDCONF=ignore
%{?scl:scl enable %{scl} "}
ocaml setup.ml -install
%{?scl:"}

%files
%doc README.md LICENSE CHANGES.md
%{_bindir}/utop
%{_bindir}/utop-full
%{_libdir}/ocaml/utop/*
%{_scl_root}/usr/share/emacs/site-lisp/utop.el

%changelog
* Tue Dec 9 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.16-1
- SCLify

* Mon May 12 2014 David Scott <dave.scott@citrix.com> - 1.12-1
- Update to 1.12

* Fri Jun 21 2013 David Scott <dave.scott@eu.citrix.com> - 1.5-1
- Update to version 1.5 (discovered lurking in plain sight on github)

* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package

