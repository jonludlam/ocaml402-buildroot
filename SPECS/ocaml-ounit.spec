# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml4021 in this case
%global scl ocaml4021
%endif

%{?scl:%scl_package ocaml-ounit}
%{!?scl:%global pkg_name %{name}}

%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}ocaml-ounit
Version:        2.0.0
Release:        10%{?dist}
Summary:        Unit test framework for OCaml

License:        MIT
URL:            http://ounit.forge.ocamlcore.org/
Source0:        http://forge.ocamlcore.org/frs/download.php/1258/ounit-%{version}.tar.gz
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  %{?scl_prefix}ocaml >= 3.10.0
BuildRequires:  %{?scl_prefix}ocaml-findlib-devel
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif
# This may have been required by < 2.0.0, but doesn't seem to be
# needed for newer versions.
#BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel


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
%{?scl:scl enable %{scl} "}
sh ./configure --destdir $RPM_BUILD_ROOT
%{?scl:"}

%build
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
* Mon Dec 1 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 2.0.0-10
- SCLify

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-9
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-8
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-6
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Thu Jul 17 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-5
- OCaml 4.02.0 beta rebuild.

* Mon Jul 14 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-4
- Remove workaround for code gen bug and try building against
  possibly fixed compiler.

* Sun Jul 13 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-3
- Add workaround for code generator bug on ARM (RHBZ#1119049).

* Sat Jul 12 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-1
- New upstream version 2.0.0.
- Remove BR on camlp4.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-8
- Rebuild for updated Arg module (RHBZ#1065447).

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-7
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-4
- Rebuild for OCaml 4.00.1.
- Clean up the spec file.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-3
- Bump and rebuild against new OCaml 4.00.0 official release.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-1
- New upstream version 1.1.2, fixed for OCaml 4.00.0.

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-6
- Rebuild for OCaml 4.00.0.

* Mon May 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-5
- Bump release and rebuild for new OCaml on ARM.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-4
- Rebuild for OCaml 3.12.1.

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
