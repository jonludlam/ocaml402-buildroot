%global scl jonludlam-ocaml4021
%{?scl:%scl_package ocaml-variantslib}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} /usr/lib/rpm/ocaml-find-requires.sh -c
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocaml-variantslib
Version:        109.15.02
Release:        2%{?dist}
Summary:        OCaml variants as first class values

Group:          Development/Libraries
License:        Apache Software License 2.0
URL:            https://github.com/janestreet/variantslib
Source0:        https://ocaml.janestreet.com/ocaml-core/109.15.00/individual/variantslib-%{version}.tar.gz
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  %{?scl_prefix}ocaml >= 4.00.1
BuildRequires:  %{?scl_prefix}ocaml-findlib-devel
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-type-conv >= 109.53.02
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
OCaml variants as first class values.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n variantslib-%{version}

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
      --sharedstatedir %{_sharedstatedir} \
      --destdir $RPM_BUILD_ROOT
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
%doc COPYRIGHT.txt LICENSE.txt  THIRD-PARTY.txt INRIA-DISCLAIMER.txt
%{_libdir}/ocaml/variantslib
%if %opt
%exclude %{_libdir}/ocaml/variantslib/*.a
%exclude %{_libdir}/ocaml/variantslib/*.cmxa
%endif
%exclude %{_libdir}/ocaml/variantslib/*.mli


%files devel
%defattr(-,root,root,-)
%doc COPYRIGHT.txt LICENSE.txt THIRD-PARTY.txt INRIA-DISCLAIMER.txt README.txt
%if %opt
%{_libdir}/ocaml/variantslib/*.a
%{_libdir}/ocaml/variantslib/*.cmxa
%endif
%{_libdir}/ocaml/variantslib/*.mli


%changelog
* Wed Dec 3 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 109.15.02-2
- SCLify

* Wed Jan 01 2014 Edvard Fagerholm <edvard.fagerholm@gmail.com> - 109.15.02-1
- Initial package for Fedora 20.
