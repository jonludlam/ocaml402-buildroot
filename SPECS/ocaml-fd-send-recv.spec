# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-fd-send-recv}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocaml-fd-send-recv
Version:        1.0.1
Release:        3%{?dist}
Summary:        Bindings to sendmsg/recvmsg for fd passing under Linux
License:        LGPL
URL:            https://github.com/xapi-project/ocaml-fd-send-recv
Source0:        https://github.com/xapi-project/ocaml-fd-send-recv/archive/ocaml-fd-send-recv-%{version}/ocaml-fd-send-recv-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif


%description
Bindings to sendmsg/recvmsg for fd passing under Linux.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocaml-fd-send-recv-ocaml-fd-send-recv-%{version}

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure
ocaml setup.ml -build
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
mkdir -p $OCAMLFIND_DESTDIR/stublibs
export OCAMLFIND_LDCONF=ignore
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%doc LICENSE
%doc README.md
%{_libdir}/ocaml/fd-send-recv
%exclude %{_libdir}/ocaml/fd-send-recv/*.a
%exclude %{_libdir}/ocaml/fd-send-recv/*.cmxa
%exclude %{_libdir}/ocaml/fd-send-recv/*.cmx
%exclude %{_libdir}/ocaml/fd-send-recv/*.mli
%{_libdir}/ocaml/stublibs/dllfd_send_recv_stubs.so
%{_libdir}/ocaml/stublibs/dllfd_send_recv_stubs.so.owner

%files devel
%{_libdir}/ocaml/fd-send-recv/*.a
%{_libdir}/ocaml/fd-send-recv/*.cmx
%{_libdir}/ocaml/fd-send-recv/*.cmxa
%{_libdir}/ocaml/fd-send-recv/*.mli

%changelog
* Mon Mar 23 2015 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.0.1-3
- SCLify

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 1.0.1-2
- Split files correctly between base and devel packages

* Fri May 31 2013 David Scott <dave.scott@eu.citrix.com> - 1.0.1-1
- Initial package

