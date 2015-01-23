# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-biniou}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}ocaml-biniou
Version:        1.0.6
Release:        4%{?dist}
Summary:        Compact, fast and extensible serialization format
License:        BSD3
URL:            http://mjambon.com/biniou.html
Source0:        https://github.com/mjambon/biniou/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-easy-format-devel
BuildRequires:  %{?scl_prefix}ocaml-findlib
Obsoletes:      biniou <= 1.0.6

%description
Binary data format designed for speed, safety, ease of use and backward
compatibility as protocols evolve.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n biniou-%{version}

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
mkdir -p %{buildroot}/%{_bindir}
%{?scl:scl enable %{scl} "}
make install BINDIR=%{buildroot}/%{_bindir}
%{?scl:"}

%files
%doc LICENSE
%doc README.md
%{_bindir}/bdump
%{_libdir}/ocaml/biniou
%exclude %{_libdir}/ocaml/biniou/*.a
%exclude %{_libdir}/ocaml/biniou/*.cmxa
%exclude %{_libdir}/ocaml/biniou/*.cmx
%exclude %{_libdir}/ocaml/biniou/*.mli

%files devel
%{_libdir}/ocaml/biniou/*.a
%{_libdir}/ocaml/biniou/*.cmx
%{_libdir}/ocaml/biniou/*.cmxa
%{_libdir}/ocaml/biniou/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.0.6-4
- SCLify

* Tue Oct 21 2014 Euan Harris <euan.harris@citrix.com> - 1.0.6-3
- Switch to GitHub sources

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 1.0.6-2
- Split files correctly between base and devel packages

* Fri May 31 2013 David Scott <dave.scott@eu.citrix.com> - 1.0.6-1
- Initial package

