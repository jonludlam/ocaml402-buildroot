%{?scl:%scl_package ocaml-ounit}
%{!?scl:%global pkg_name %{name}}

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%define debug_package %{nil}

Name:           %{?scl_prefix}ocaml-ounit
Version:        2.0.0
Release:        1%{?dist}
Summary:        Unit test framework for OCaml

License:        MIT
URL:            http://ounit.forge.ocamlcore.org/
Source0:        http://forge.ocamlcore.org/frs/download.php/1258/ounit-%{version}.tar.gz
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  %{?scl_prefix}ocaml >= 3.10.0
BuildRequires:  %{?scl_prefix}ocaml-findlib-devel
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc

%description
OUnit is a unit test framework for OCaml. It allows one to easily
create unit-tests for OCaml code. It is based on HUnit, a unit testing
framework for Haskell. It is similar to JUnit, and other xUnit testing
frameworks.

%package        devel
Summary:        Development files for %{pkg_name}
Requires:       %{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description    devel
The %{pkg_name}-devel package contains libraries and signature files for
developing applications that use %{pkg_name}.

%prep
%setup -q -n ounit-%{version}

%build
sh ./configure --destdir $RPM_BUILD_ROOT
%{?scl:scl enable %{scl} "}
make all
%{?scl:"}
%{?scl:scl enable %{scl} "}
make doc
%{?scl:"}

%check
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

# Remove this, reinstall it properly with a %%doc rule below.
rm -rf $RPM_BUILD_ROOT/usr/local/share/doc

%files
%doc LICENSE.txt
%{_libdir}/ocaml/oUnit
%if %opt
%exclude %{_libdir}/ocaml/oUnit/*.a
%exclude %{_libdir}/ocaml/oUnit/*.cmxa
%endif
%exclude %{_libdir}/ocaml/oUnit/*.mli

%files devel
%doc LICENSE.txt README.txt
%doc _build/src/api-ounit.docdir/*
%if %opt
%{_libdir}/ocaml/oUnit/*.a
%{_libdir}/ocaml/oUnit/*.cmxa
%endif
%{_libdir}/ocaml/oUnit/*.mli

%changelog
* Tue Mar 25 2014 Euan Harris <euan.harris@citrix.com> - 2.0.0-1
- Update to version 2.0.0

* Fri Sep 30 2011 Mike McClurg <mike.mcclurg@citrix.com> - 1.1.2-3
- Repackaged for XenSource build system

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-2
- New upstream version 1.1.0.
- Project has moved to new upstream URL and Source0.
- Rebuild for OCaml 3.12.0.
- New build system:
    + doesn't need 'make allopt'
    + DESTDIR logic changed (see OASIS bug 852)
    + docdir moved
- LICENSE and README files renamed.
- BR camlp4.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-7
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-1
- New upstream version 1.0.3.

* Mon May 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-2
- License is MIT.

* Sat May  3 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-1
- Initial RPM release.

