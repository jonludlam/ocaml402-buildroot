# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-oclock}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}ocaml-oclock
Version:        0.3
Release:        4%{?dist}
Summary:        POSIX monotonic clock for OCaml
License:        ISC
URL:            https://github.com/polazarus/oclock
Source0:        https://github.com/polazarus/oclock/archive/v0.3/oclock-%{version}.tar.gz
Patch0:         oclock-1-cc-headers
Patch1:         oclock-2-destdir
Patch2:         oclock-build-id-fix
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib

%description
A POSIX monotonic clock for OCaml

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n oclock-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}

%install
export OCAMLFIND_DISTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DISTDIR
mkdir -p $OCAMLFIND_DISTDIR/stublibs
export OCAMLFIND_LDCONF=ignore
%{?scl:scl enable %{scl} "}
make install DESTDIR=%{buildroot}/%{_libdir}/ocaml
%{?scl:"}

%files
%doc LICENSE
%doc README.markdown
%{_libdir}/ocaml/oclock
%exclude %{_libdir}/ocaml/oclock/*.a
%exclude %{_libdir}/ocaml/oclock/*.cmxa
%{_libdir}/ocaml/stublibs/dlloclock.so
%{_libdir}/ocaml/stublibs/dlloclock.so.owner

%files devel
%{_libdir}/ocaml/oclock/*.a
%{_libdir}/ocaml/oclock/*.cmxa

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.3-4
- SCLify

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 0.3-3
- Split files correctly between base and devel packages

* Wed May 29 2013 David Scott <dave.scott@eu.citrix.com> - 0.3-2
- Initial package

