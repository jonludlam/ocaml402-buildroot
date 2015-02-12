# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-easy-format}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}ocaml-easy-format
Version:        1.0.1
Release:        4%{?dist}
Summary:        Indentation made easy
License:        BSD
URL:            http://mjambon.com/easy-format.html
Source0:        https://github.com/mjambon/easy-format/archive/v%{version}/ocaml-easy-format-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib
Obsoletes:      easy-format <= 1.0.1

%description
Easy_format: indentation made easy.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n easy-format-%{version}

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
%doc LICENSE
%doc README
%{_libdir}/ocaml/easy-format
%exclude %{_libdir}/ocaml/easy-format/*.cmx
%exclude %{_libdir}/ocaml/easy-format/*.mli

%files devel
%{_libdir}/ocaml/easy-format/*.cmx
%{_libdir}/ocaml/easy-format/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> 1.0.1-4
- SCLify

* Tue Oct 21 2014 Euan Harris <euan.harris@citrix.com> - 1.0.1-3
- Switch to GitHub sources

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 1.0.1-2
- Split files correctly between base and devel packages

* Fri May 31 2013 David Scott <dave.scott@eu.citrix.com> - 1.0.1-1
- Initial package

