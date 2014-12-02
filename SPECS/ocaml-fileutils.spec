%global scl jonludlam-ocaml4021
%{?scl:%scl_package ocaml-fileutils}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} /usr/lib/rpm/ocaml-find-requires.sh -c
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocaml-fileutils
Version:        0.4.5
Release:        11%{?dist}
Summary:        OCaml library for common file and filename operations

License:        LGPLv2 with exceptions
URL:            https://forge.ocamlcore.org/projects/ocaml-fileutils/
Source0:        https://forge.ocamlcore.org/frs/download.php/1194/ocaml-fileutils-%{version}.tar.gz
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  %{?scl_prefix}ocaml >= 4.00.1
BuildRequires:  %{?scl_prefix}ocaml-findlib-devel >= 1.3.3-3
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
%if 0%{?fedora} || 0%{?rhel} <= 6
BuildRequires:  %{?scl_prefix}ocaml-ounit-devel
%endif

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
This library is intended to provide a basic interface to the most
common file and filename operations.  It provides several different
filename functions: reduce, make_absolute, make_relative...  It also
enables you to manipulate real files: cp, mv, rm, touch...

It is separated into two modules: SysUtil and SysPath.  The first one
manipulates real files, the second one is made for manipulating
abstract filenames.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n %{pkg_name}-%{version}

# Disable the tests (RHEL 7 only) since they require ocaml-ounit.
%if 0%{?rhel} >= 7
rm test/test.ml
touch test/test.ml
mv setup.ml setup.ml.old
sed '/oUnit/d' < setup.ml.old > setup.ml
%endif


%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure --prefix %{_prefix} --destdir $RPM_BUILD_ROOT
make
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=\$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p \$OCAMLFIND_DESTDIR \$OCAMLFIND_DESTDIR/stublibs

# Set htmldir to current directory, then copy the docs (in api/)
# as a %doc rule.
make htmldir=. install
%{?scl:"}


%check
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}


%files
%doc COPYING.txt
%{_libdir}/ocaml/fileutils
%if %opt
%exclude %{_libdir}/ocaml/fileutils/*.a
%exclude %{_libdir}/ocaml/fileutils/*.cmx
%exclude %{_libdir}/ocaml/fileutils/*.cmxa
%endif
%exclude %{_libdir}/ocaml/fileutils/*.ml
%exclude %{_libdir}/ocaml/fileutils/*.mli


%files devel
%doc COPYING.txt AUTHORS.txt CHANGELOG.txt README.txt TODO.txt
%if %opt
%{_libdir}/ocaml/fileutils/*.a
%{_libdir}/ocaml/fileutils/*.cmx
%{_libdir}/ocaml/fileutils/*.cmxa
%endif
%{_libdir}/ocaml/fileutils/*.ml
%{_libdir}/ocaml/fileutils/*.mli


%changelog
* Tue Dec 2 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.4.5-11
- SCLify

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-10
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-9
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-7
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-6
- OCaml 4.02.0 beta rebuild.

* Mon Jul 14 2014 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-5
- Rebuild for OCaml 4.02.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-1
- New upstream version 0.4.5.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.4-4
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.4-3
- Disable the tests on RHEL 7, since they require ocaml-ounit.

* Fri Oct 19 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.4-2
- New upstream version 0.4.4.
- Clean up the spec file.
- Fix homepage and download URLs.
- Don't use configure macro.  Upstream are using some sort of non-autoconf
  brokenness.
- Rename text files as *.txt.  There is no 'api' directory any more.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-10
- Bump and rebuild against new OCaml 4.00.0 official release.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-8
- Rebuild for OCaml 4.00.0.

* Mon May 14 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-7
- Bump release and rebuild for new OCaml on ARM.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-6
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-4
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-3
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-2
- New upstream version 0.4.0.
- Upstream build system has been rationalized, so remove all the
  hacks we were using.
- Upstream now contains tests, run them.
- Needs ounit in order to carry out the tests.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-10
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-8
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-7
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-5
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-4
- Rebuild for ppc64.

* Thu Feb 21 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-3
- Fixed grammar in the description section.
- License is LGPLv2 with exceptions
- Include license file with both RPMs.
- Include other documentation only in the -devel RPM.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-2
- Added BR ocaml-camlp4-devel.
- Build into tmp directory under the build root.

* Wed Aug  8 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-1
- Initial RPM release.
