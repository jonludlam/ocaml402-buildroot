# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml4021 in this case
%global scl ocaml4021
%endif

%{?scl:%scl_package ocaml-react}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocaml-react
Version:        1.1.0
Release:        3%{?dist}
Summary:        OCaml framework for Functional Reactive Programming (FRP)
License:        BSD
URL:            http://erratique.ch/software/react
Source0:        https://github.com/dbuenzli/react/archive/v%{version}/react-%{version}.tar.gz
Source1:        react-LICENSE

ExclusiveArch:  x86_64

BuildRequires:  %{?scl_prefix}ocaml >= 3.11.0
BuildRequires:  %{?scl_prefix}ocaml-findlib-devel
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
React is an OCaml module for functional reactive programming (FRP). It
provides support to program with time varying values : applicative
events and signals. React doesn't define any primitive event or
signal, this lets the client chooses the concrete timeline.

React is made of a single, independent, module and distributed under
the new BSD license.

Given an absolute notion of time Rtime helps you to manage a timeline
and provides time stamp events, delayed events and delayed signals.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n react-%{version}
cp -p %{SOURCE1} LICENSE

%build
%{?scl:scl enable %{scl} "}
ocaml pkg/build.ml native=true native-dynlink=true
%{?scl:"}


%install
mkdir -p %{buildroot}/%{_libdir}/ocaml/react
cp _build/pkg/META _build/src/react.a _build/src/react.cma _build/src/react.cmi _build/src/react.cmx _build/src/react.cmxa _build/src/react.cmxs _build/src/react.mli %{buildroot}/%{_libdir}/ocaml/react

%files
%doc LICENSE
%{_libdir}/ocaml/react
%if %opt
%exclude %{_libdir}/ocaml/react/*.cmx
%endif
%exclude %{_libdir}/ocaml/react/*.mli


%files devel
%doc CHANGES.md README.md
%if %opt
%{_libdir}/ocaml/react/*.cmx
%endif
%{_libdir}/ocaml/react/*.mli


%changelog
* Fri Dec 5 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.1.0-3
- New upstream version 1.1.0
- SCLify

* Wed Sep 18 2013 Jerry James <loganjerry@gmail.com>
- Rebuild for OCaml 4.01.0
- Enable debuginfo
- Add missing ExclusiveArch
- Minor spec file cleanups

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-1
- New upstream version 0.9.4.
- Rebuild for OCaml 4.00.1.
- Clean up the spec file.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.2-4
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.2-3
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 0.9.2-1
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-3
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-2
- Initial RPM release.
- Use global instead of define (Till Maas).
