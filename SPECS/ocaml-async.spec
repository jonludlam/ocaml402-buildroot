# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml4021 in this case
%global scl ocaml4021
%endif

%{?scl:%scl_package ocaml-async-unix}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocaml-async
Version:        112.01.00
Release:        1%{?dist}
Summary:        Jane Street Capital's asynchronous execution library (core)

Group:          Development/Libraries
License:        Apache Software License 2.0
URL:            https://github.com/janestreet/async
Source0:        https://ocaml.janestreet.com/ocaml-core/%{version}/individual/async-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  %{?scl_prefix}ocaml >= 4.00.1
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-async-kernel-devel
BuildRequires:  %{?scl_prefix}ocaml-async-unix-devel
BuildRequires:  %{?scl_prefix}ocaml-async-extra-devel
BuildRequires:  %{?scl_prefix}ocaml-ounit-devel
BuildRequires:  %{?scl_prefix}ocaml-findlib-devel
BuildRequires:  %{?scl_prefix}ocaml-comparelib-devel
BuildRequires:  %{?scl_prefix}ocaml-enumerate-devel
BuildRequires:  %{?scl_prefix}ocaml-herelib-devel
BuildRequires:  %{?scl_prefix}ocaml-custom-printf-devel

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
Jane Street Capital's asynchronous execution library (core).

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:  %{?scl_prefix}ocaml-async-kernel-devel
Requires:  %{?scl_prefix}ocaml-async-unix-devel
Requires:  %{?scl_prefix}ocaml-async-extra-devel
Requires:  %{?scl_prefix}ocaml-ounit-devel
Requires:  %{?scl_prefix}ocaml-findlib-devel
Requires:  %{?scl_prefix}ocaml-comparelib-devel
Requires:  %{?scl_prefix}ocaml-enumerate-devel
Requires:  %{?scl_prefix}ocaml-herelib-devel
Requires:  %{?scl_prefix}ocaml-custom-printf-devel

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n async-%{version}

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
%doc LICENSE.txt THIRD-PARTY.txt INRIA-DISCLAIMER.txt
%{_libdir}/ocaml/async
%if %opt
%exclude %{_libdir}/ocaml/async/*.a
%exclude %{_libdir}/ocaml/async/*.cmxa
%endif
%exclude %{_libdir}/ocaml/async/*.ml

%files devel
%defattr(-,root,root,-)
%doc LICENSE.txt THIRD-PARTY.txt INRIA-DISCLAIMER.txt
%if %opt
%{_libdir}/ocaml/async/*.a
%{_libdir}/ocaml/async/*.cmxa
%endif
%{_libdir}/ocaml/async/*.ml

%changelog
* Tue Dec 9 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 112.01.00-1
- Update to 112.01.00 and SCLify

* Tue Oct 14 2014 David Scott <dave.scott@citrix.com> - 111.25.00-1
- Update to 111.25.00

* Wed Jan 01 2014 Edvard Fagerholm <edvard.fagerholm@gmail.com> - 109.53.02-1
- Initial package for Fedora 20.
