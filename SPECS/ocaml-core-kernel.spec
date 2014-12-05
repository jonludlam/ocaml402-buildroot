# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml4021 in this case
%global scl ocaml4021
%endif

%{?scl:%scl_package ocaml-core-kernel}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocaml-core-kernel
Version:        112.01.00
Release:        1%{?dist}
Summary:        System-independent part of Jane Street's Core.

Group:          Development/Libraries
License:        Apache Software License 2.0
URL:            https://github.com/janestreet/core_kernel
Source0:        https://ocaml.janestreet.com/ocaml-core/%{version}/individual/core_kernel-%{version}.tar.gz
Patch0:         fix-hash-stubs
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  %{?scl_prefix}ocaml >= 4.00.1
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-findlib-devel
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-bin-prot-devel
BuildRequires:  %{?scl_prefix}ocaml-comparelib-devel
BuildRequires:  %{?scl_prefix}ocaml-fieldslib-devel
BuildRequires:  %{?scl_prefix}ocaml-herelib-devel
BuildRequires:  %{?scl_prefix}ocaml-pa-bench-devel
BuildRequires:  %{?scl_prefix}ocaml-pa-ounit-devel
BuildRequires:  %{?scl_prefix}ocaml-pa-pipebang-devel
BuildRequires:  %{?scl_prefix}ocaml-pa-test-devel
BuildRequires:  %{?scl_prefix}ocaml-enumerate-devel
BuildRequires:  %{?scl_prefix}ocaml-sexplib-devel
BuildRequires:  %{?scl_prefix}ocaml-typerep-devel
BuildRequires:  %{?scl_prefix}ocaml-variantslib-devel
BuildRequires:  chrpath

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
Core is an industrial-strength alternative to the OCaml standard
library.  It was developed by Jane Street, which is the largest
industrial user of OCaml. Core_kernel is the system-independent
part of Core.  It is aimed for cases when the full Core is not
available, such as in Javascript.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n core_kernel-%{version}
%patch0 -p1 

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
strip $OCAMLFIND_DESTDIR/stublibs/dll*.so
chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dll*.so

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYRIGHT.txt LICENSE.txt THIRD-PARTY.txt INRIA-DISCLAIMER.txt MLton-license.txt
%{_libdir}/ocaml/core_kernel
%if %opt
%exclude %{_libdir}/ocaml/core_kernel/*.a
%exclude %{_libdir}/ocaml/core_kernel/*.cmxa
%endif
%exclude %{_libdir}/ocaml/core_kernel/*.ml
%exclude %{_libdir}/ocaml/core_kernel/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner

%files devel
%defattr(-,root,root,-)
%doc COPYRIGHT.txt LICENSE.txt THIRD-PARTY.txt INRIA-DISCLAIMER.txt README.md MLton-license.txt
%if %opt
%{_libdir}/ocaml/core_kernel/*.a
%{_libdir}/ocaml/core_kernel/*.cmxa
%endif
%{_libdir}/ocaml/core_kernel/*.ml
%{_libdir}/ocaml/core_kernel/*.mli

%changelog
* Thu Dec 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 112.01.00-1
- Update to 112.01.00

* Wed Dec 3 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 111.28.00-2
- SCLify

* Tue Oct 14 2014 David Scott <dave.scott@citrix.com> - 111.28.00-1
- Update to 111.28.00

* Wed Jan 01 2014 Edvard Fagerholm <edvard.fagerholm@gmail.com> - 109.55.02-1
- Initial package for Fedora 20.
