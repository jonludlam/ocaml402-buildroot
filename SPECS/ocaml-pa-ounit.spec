%global scl jonludlam-ocaml4021
%{?scl:%scl_package ocaml-pa-ounit}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} /usr/lib/rpm/ocaml-find-requires.sh -c
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocaml-pa-ounit
Version:        111.28.00
Release:        2%{?dist}
Summary:        Syntax extension for in-line tests in code.

Group:          Development/Libraries
License:        Apache Software License 2.0
URL:            https://github.com/janestreet/pa_ounit
Source0:        https://ocaml.janestreet.com/ocaml-core/%{version}/individual/pa_ounit-%{version}.tar.gz
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  %{?scl_prefix}ocaml >= 4.00.1
BuildRequires:  %{?scl_prefix}ocaml-findlib-devel
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-ounit-devel

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
Pa_ounit is a syntax extension that helps writing in-line tests in ocaml code.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n pa_ounit-%{version}

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure --prefix %{_prefix} \
      --libdir %{_libdir} \
      --libexecdir %{_libexecdir} \
      --exec-prefix %{_exec_prefix} \
      --bindir %{_bindir} \
      --sbindir %{_sbindir} \
      --mandir %{_mandir} \
      --datadir %{_datadir} \
      --localstatedir %{_localstatedir} \
      --sharedstatedir %{_sharedstatedir}
ocaml setup.ml -build
%{?scl:"}


%check
%{?scl:scl enable %{scl} "}
ocaml setup.ml -test
%{?scl:"}


%install
rm -rf $RPM_BUILD_ROOT
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%{?scl:scl enable %{scl} "}
ocaml setup.ml -install
%{?scl:"}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.txt  THIRD-PARTY.txt INRIA-DISCLAIMER.txt readme.md
%{_libdir}/ocaml/pa_ounit
%if %opt
%exclude %{_libdir}/ocaml/pa_ounit/*.a
%exclude %{_libdir}/ocaml/pa_ounit/*.cmxa
%endif
%exclude %{_libdir}/ocaml/pa_ounit/*.ml
%exclude %{_libdir}/ocaml/pa_ounit/*.mli


%files devel
%defattr(-,root,root,-)
%doc LICENSE.txt  THIRD-PARTY.txt INRIA-DISCLAIMER.txt readme.md
%if %opt
%{_libdir}/ocaml/pa_ounit/*.a
%{_libdir}/ocaml/pa_ounit/*.cmxa
%endif
%{_libdir}/ocaml/pa_ounit/*.ml
%{_libdir}/ocaml/pa_ounit/*.mli


%changelog
* Wed Dec 3 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 111.28.00-2
- SCLify

* Tue Oct 14 2014 David Scott <dave.scott@citrix.com> - 111.28.00-1
- Update to 111.28.00

* Wed Jan 01 2014 Edvard Fagerholm <edvard.fagerholm@gmail.com> - 109.53.02-1
- Initial package for Fedora 20
