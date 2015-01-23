# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-camlp4}
%{!?scl:%global pkg_name %{name}}

%define ocaml_native_compiler x86_64
%define ocaml_natdynlink x86_64

%ifarch %{ocaml_native_compiler}
%global native_compiler 1
%else
%global native_compiler 0
%endif

%global gitcommit 87c6a6b07818acbbef6ced00cc8f4e09b533e055
%global shortcommit 87c6a6b0

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:          %{?scl_prefix}ocaml-camlp4
Version:       4.02.0
Release:       0.9.git%{shortcommit}%{?dist}

Summary:       Pre-Processor-Pretty-Printer for OCaml

License:       LGPLv2+ with exceptions

URL:           https://github.com/ocaml/camlp4
Source0:       https://github.com/ocaml/camlp4/archive/%{gitcommit}/camlp4-%{gitcommit}.tar.gz

# This causes the RPMs to be explicitly SCL ones.
%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif
 
# This package used to be part of the upstream compiler.  We still
# need to keep it in lock step with the compiler, so whenever a new
# compiler is released we will also update this package also.
BuildRequires: %{?scl_prefix}ocaml
Requires:      %{?scl_prefix}ocaml-runtime


%description
Camlp4 is a Pre-Processor-Pretty-Printer for OCaml, parsing a source
file and printing some result on standard output.

This package contains the runtime files.


%package devel
Summary:       Pre-Processor-Pretty-Printer for OCaml

Requires:      %{?scl_prefix}%{pkg_name}%{?_isa} = %{version}-%{release}


%description devel
Camlp4 is a Pre-Processor-Pretty-Printer for OCaml, parsing a source
file and printing some result on standard output.

This package contains the development files.


%prep
%setup -q -n camlp4-%{gitcommit}


%build
%{?scl:scl enable %{scl} "}
./configure
%{?scl:"}
# Incompatible with parallel builds:
unset MAKEFLAGS
%if !%{native_compiler}
%{?scl:scl enable %{scl} "}
make byte
%{?scl:"}
%else
%{?scl:scl enable %{scl} "}
make all
%{?scl:"}
%endif


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/camlp4
%{?scl:scl enable %{scl} - << \EOF}
make install \
  BINDIR=$RPM_BUILD_ROOT%{_bindir} \
  LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
  PKGDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/camlp4
%{?scl:EOF}


%files
%doc README.md LICENSE
%dir %{_libdir}/ocaml/camlp4
%{_libdir}/ocaml/camlp4/*.cmi
%{_libdir}/ocaml/camlp4/*.cma
%{_libdir}/ocaml/camlp4/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Filters
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Parsers
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmo
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmi
%dir %{_libdir}/ocaml/camlp4/Camlp4Printers
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Top
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmo


%files devel
%doc LICENSE
%{_bindir}/camlp4*
%{_bindir}/mkcamlp4
%if %{native_compiler}
%{_libdir}/ocaml/camlp4/*.a
%{_libdir}/ocaml/camlp4/*.cmxa
%{_libdir}/ocaml/camlp4/*.cmx
%{_libdir}/ocaml/camlp4/*.o
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.o
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.o
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.o
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Top/*.o
%endif

%changelog
* Thu Nov 27 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 4.02.0-0.9.git87c6a6b0
- SCLify

* Mon Nov 03 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.8.git87c6a6b0
- Bump version and rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.7.git87c6a6b0
- ocaml-4.02.0 final rebuild.

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.6.git87c6a6b0
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.02.0-0.5.git87c6a6b0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.4.git87c6a6b0
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Sat Jul 19 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.3.git87c6a6b0
- OCaml 4.02.0 beta rebuild.

* Wed Jul 16 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.2
- Initial packaging of new out-of-tree ocaml-camlp4.
