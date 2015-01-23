# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-ctypes}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}ocaml-ctypes
Version:        0.2.2
Release:        2%{?dist}
Summary:        Library for binding to C libraries using pure OCaml
License:        MIT
URL:            https://github.com/ocamllabs/ocaml-ctypes/
Source0:        https://github.com/ocamllabs/ocaml-ctypes/archive/ocaml-ctypes-%{version}.tar.gz
Patch0:         ocaml-ctypes-0.2.1-std-gnu99.patch
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  libffi-devel

%description
Library for binding to C libraries using pure OCaml

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocaml-ctypes-ocaml-ctypes-%{version}
%patch0 -p1

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}

%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
export OCAMLFIND_LDCONF=ignore
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}/ocaml
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%doc README.md LICENSE CHANGES
%{_libdir}/ocaml/ctypes
%exclude %{_libdir}/ocaml/ctypes/*.a
%exclude %{_libdir}/ocaml/ctypes/*.cmxa
%exclude %{_libdir}/ocaml/ctypes/*.cmx
%exclude %{_libdir}/ocaml/ctypes/*.mli

%files devel
%{_libdir}/ocaml/ctypes/*.a
%{_libdir}/ocaml/ctypes/*.cmx
%{_libdir}/ocaml/ctypes/*.cmxa
%{_libdir}/ocaml/ctypes/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.2.2-2
- SCLify

* Thu Apr 24 2014 David Scott <dave.scott@citrix.com>
- Fix the split between devel and main package, hopefully

* Wed Nov 13 2013 Mike McClurg <mike.mcclurg@citrix.com>
- Initial package

