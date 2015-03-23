# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-uri}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

# Note - these two lines backported from Fedora
%global ocaml_native_compiler aarch64 %{arm} %{ix86} ppc ppc64 ppc64le sparc sparcv9 x86_64
%global ocaml_natdynlink      aarch64 %{arm} %{ix86} ppc ppc64 ppc64le sparc sparcv9 x86_64

%ifarch %{ocaml_native_compiler}
%global native_compiler 1
%else
%global native_compiler 0
%endif

Name:           %{?scl_prefix}ocaml-uri
Version:        1.6.0
Release:        2%{?dist}
Summary:        A URI library for OCaml
License:        ISC
URL:            https://github.com/mirage/ocaml-uri
Source0:        https://github.com/mirage/ocaml-uri/archive/v%{version}/ocaml-uri-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml >= 4.00
BuildRequires:  %{?scl_prefix}ocaml-compiler-libs
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-ounit-devel
BuildRequires:  %{?scl_prefix}ocaml-re-devel
BuildRequires:  %{?scl_prefix}ocaml-stringext-devel
BuildRequires:  %{?scl_prefix}ocaml-sexplib-devel

%description
A URI library for OCaml.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}ocaml-re-devel%{?_isa}
Requires:       %{?scl_prefix}ocaml-stringext-devel%{?_isa}
Requires:       %{?scl_prefix}ocaml-sexplib-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocaml-uri-%{version}

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure --destdir %{buildroot}/%{_libdir}/ocaml
make
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}
rm -rf %{buildroot}/%{_libdir}/ocaml/usr

%files
%doc CHANGES
%doc README.md 
%{_libdir}/ocaml/uri
%exclude %{_libdir}/ocaml/uri/*.a
%exclude %{_libdir}/ocaml/uri/*.cmxa
%exclude %{_libdir}/ocaml/uri/*.cmx
%exclude %{_libdir}/ocaml/uri/*.mli

%files devel
%doc uri.docdir/*
%{_libdir}/ocaml/uri/*.a
%{_libdir}/ocaml/uri/*.cmx
%{_libdir}/ocaml/uri/*.cmxa
%{_libdir}/ocaml/uri/*.mli

%changelog
* Sun Mar 08 2015 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.6.0-2
- SCLify

* Fri Jun 06 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.6.0-1
- Update to 1.6.0

* Mon Jun 02 2014 David Scott <dave.scott@eu.citrix.com> - 1.3.8-2
- Split files correctly between base and devel packages

* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com> - 1.3.8-1
- Initial package

