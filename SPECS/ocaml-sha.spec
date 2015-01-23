# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-sha}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif


Name:           %{?scl_prefix}ocaml-sha
Version:        1.9
Release:        3%{?dist}
Summary:        OCaml SHA
License:        LGPL2.1
URL:            https://github.com/vincenthz/ocaml-sha
Source0:        https://github.com/vincenthz/ocaml-sha/archive/ocaml-sha-v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib

%description
This is a set of C bindings for computing SHA digests.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocaml-sha-ocaml-sha-v%{version}

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}%{_libdir}/ocaml
export OCAMLFIND_LDCONF=%{buildroot}%{_libdir}/ocaml/ld.conf
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%doc README
%{_libdir}/ocaml/sha
%exclude %{_libdir}/ocaml/sha/*.a
%exclude %{_libdir}/ocaml/sha/*.cmxa
%exclude %{_libdir}/ocaml/sha/*.cmx

%files devel
%{_libdir}/ocaml/sha/*.a
%{_libdir}/ocaml/sha/*.cmx
%{_libdir}/ocaml/sha/*.cmxa

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.6-3
- SCLify

* Tue Apr 22 2014 Euan Harris <euan.harris@citrix.com> - 1.9-2
- Split files correctly between base and devel packages

* Mon Nov 18 2013 David Scott <dave.scott@eu.citrix.com> - 1.9-1
- Initial package

