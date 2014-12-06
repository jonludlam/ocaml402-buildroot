# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml4021 in this case
%global scl ocaml4021
%endif

%{?scl:%scl_package ocaml-text}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocaml-text
Version:        0.7.1
Release:        2%{?dist}
Summary:        Library for dealing with unicode text conveniently

License:        BSD
URL:            https://github.com/vbmithr/ocaml-text
Source0:        https://github.com/vbmithr/ocaml-text/archive/%{version}/ocaml-text-%{version}.tar.gz
Patch0:         uint32-patch
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  %{?scl_prefix}ocaml >= 3.10.0
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-camlp4
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
OCaml-Text is a library for dealing with ``text'', i.e. sequence of
unicode characters, in a convenient way.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocaml-text-%{version}
%patch0 -p1

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure --destdir $RPM_BUILD_ROOT --prefix /usr
make
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

# Remove this, reinstall it properly with a %%doc rule below.
rm -rf $RPM_BUILD_ROOT/usr/local/share/doc

%files
%{_libdir}/ocaml/text
%exclude %{_libdir}/ocaml/text/*.a
%exclude %{_libdir}/ocaml/text/*.cmxa
%exclude %{_libdir}/ocaml/text/*.cmx
%exclude %{_libdir}/ocaml/text/*.mli
%{_libdir}/ocaml/stublibs/dllbigarray_stubs.so
%{_libdir}/ocaml/stublibs/dllbigarray_stubs.so.owner
%{_libdir}/ocaml/stublibs/dlltext_stubs.so
%{_libdir}/ocaml/stublibs/dlltext_stubs.so.owner

%files devel
%{_libdir}/ocaml/text/*.a
%{_libdir}/ocaml/text/*.cmx
%{_libdir}/ocaml/text/*.cmxa
%{_libdir}/ocaml/text/*.mli

%changelog
* Sat Dec 6 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.7.1-2
- SCLify

* Thu Oct 2 2014 Euan Harris <euan.harris@citrix.com> - 0.7.1-1
- Update to 0.7.1 and get source from GitHub

* Mon Jun 02 2014 Euan Harris <euan.harris@citrix.com> - 0.6-2
- Split files correctly between base and devel packages

* Sat Jun 01 2013 David Scott <dave.scott@eu.citrix.com> - 0.6-1
- Initial package

