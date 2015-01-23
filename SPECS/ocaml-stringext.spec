# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-stringext}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}ocaml-stringext
Version:        0.0.1
Release:        1%{?dist}
Summary:        String manipulation functions
License:        Unknown 
Group:          Development/Libraries
URL:            http://github.com/rgrinberg/stringext
Source0:        https://github.com/rgrinberg/stringext/archive/v%{version}/stringext-%{version}.tar.gz

BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib

%description
Extra string functions for OCaml

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n stringext-%{version}


%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure
ocaml setup.ml -build
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
ocaml setup.ml -install
%{?scl:"}


%files
%{_libdir}/ocaml/stringext
%exclude %{_libdir}/ocaml/stringext/*.a
%exclude %{_libdir}/ocaml/stringext/*.cmxa
%exclude %{_libdir}/ocaml/stringext/*.cmx
%exclude %{_libdir}/ocaml/stringext/*.mli


%files devel
%{_libdir}/ocaml/stringext/*.a
%{_libdir}/ocaml/stringext/*.cmx
%{_libdir}/ocaml/stringext/*.cmxa
%{_libdir}/ocaml/stringext/*.mli

%changelog
* Fri May 2 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.0.1-1
- Initial package

