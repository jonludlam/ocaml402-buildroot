# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-async-find}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)


Name:           %{?scl_prefix}ocaml-inotify
Version:        2.0
Release:        2%{?dist}
Summary:        Inotify bindings for OCaml.

Group:          Development/Libraries
License:        Apache Software License 2.0
URL:            https://github.com/whitequark/ocaml-inotify
Source0:        https://github.com/whitequark/ocaml-inotify/archive/%{version}.tar.gz
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  %{?scl_prefix}ocaml >= 4.00.1
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-findlib-devel
BuildRequires:  chrpath


%description
Inotify bindings for OCaml.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n ocaml-inotify-%{version}

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
%doc LICENSE.txt
%doc README.md
%{_libdir}/ocaml/inotify
%if %opt
%exclude %{_libdir}/ocaml/inotify/*.a
%exclude %{_libdir}/ocaml/inotify/*.cmxa
%endif
%exclude %{_libdir}/ocaml/inotify/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner

%files devel
%defattr(-,root,root,-)
%doc LICENSE.txt
%doc README.md
%if %opt
%{_libdir}/ocaml/inotify/*.a
%{_libdir}/ocaml/inotify/*.cmxa
%endif
%{_libdir}/ocaml/inotify/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 2.0-2
- SCLify

* Tue Oct 14 2014 David Scott <dave.scott@citrix.com> - 2.0-1
- Update to 2.0

* Wed Jan 01 2014 Edvard Fagerholm <edvard.fagerholm@gmail.com> - 1.3-1
- Initial package for Fedora 20.
