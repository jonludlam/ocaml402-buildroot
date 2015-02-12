# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-yojson}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}ocaml-yojson
Version:        1.1.6
Release:        4%{?dist}
Summary:        A JSON parser and printer for OCaml
License:        BSD3
URL:            http://mjambon.com/yojson.html
Source0:        https://github.com/mjambon/yojson/archive/v%{version}/ocaml-yojson-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}cppo
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-biniou-devel
BuildRequires:  %{?scl_prefix}ocaml-easy-format-devel
BuildRequires:  %{?scl_prefix}ocaml-findlib

%description
A JSON parser and printer for OCaml.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n yojson-%{version}

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
mkdir -p %{buildroot}/%{_bindir}
%{?scl:scl enable %{scl} "}
make install DESTDIR=%{buildroot} BINDIR=%{buildroot}/%{_bindir}
%{?scl:"}

%files
%doc README.md
%doc LICENSE
%{_bindir}/ydump
%{_libdir}/ocaml/yojson
%exclude %{_libdir}/ocaml/yojson/*.cmx
%exclude %{_libdir}/ocaml/yojson/*.mli

%files devel
%{_libdir}/ocaml/yojson/*.cmx
%{_libdir}/ocaml/yojson/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.1.6-4
- SCLify

* Tue Oct 21 2014 Euan Harris <euan.harris@citrix.com> - 1.1.6-3
- Switch to GitHub sources

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 1.1.6-2
- Split files correctly between base and devel packages

* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com> - 1.1.6-1
- Initial package

