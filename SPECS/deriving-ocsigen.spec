# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package deriving-ocsigen}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}deriving-ocsigen
Version:        0.3c
Release:        3%{?dist}
Summary:        Extension to OCaml for deriving functions from type declarations
License:        MIT
URL:            http://ocsigen.org
Source0:        http://ocsigen.org/download/deriving-ocsigen-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-findlib

%description
Extension to OCaml for deriving functions from type declarations

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n deriving-ocsigen-%{version}

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%doc CHANGES
%doc COPYING
%doc README
%{_libdir}/ocaml/deriving-ocsigen
%exclude %{_libdir}/ocaml/deriving-ocsigen/*.a
%exclude %{_libdir}/ocaml/deriving-ocsigen/*.cmxa
%exclude %{_libdir}/ocaml/deriving-ocsigen/*.cmx
%exclude %{_libdir}/ocaml/deriving-ocsigen/*.mli

%files devel
%{_libdir}/ocaml/deriving-ocsigen/*.a
%{_libdir}/ocaml/deriving-ocsigen/*.cmx
%{_libdir}/ocaml/deriving-ocsigen/*.cmxa
%{_libdir}/ocaml/deriving-ocsigen/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.3c-3
- SCLify

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 0.3c-2
- Split files correctly between base and devel packages

* Fri May 31 2013 David Scott <dave.scott@eu.citrix.com> - 0.3c-1
- Initial package

