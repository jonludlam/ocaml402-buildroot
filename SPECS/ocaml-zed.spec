# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml4021 in this case
%global scl ocaml4021
%endif

%{?scl:%scl_package ocaml-zed}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}ocaml-zed
Version:        1.3
Release:        2%{?dist}
Summary:        An abstract engine for text editing for OCaml
License:        BSD3
URL:            https://github.com/diml/zed
Source0:        https://github.com/diml/zed/archive/%{version}/ocaml-zed-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-camomile-devel
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-react-devel

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
Zed is an abstract engine for text editing. It can be used for writing
text editors, editing widgets, readlines...

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}ocaml-camomile-devel%{?_isa}
Requires:       %{?scl_prefix}ocaml-react-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n zed-%{version}

%build
%{?scl:scl enable %{scl} "}
./configure
make
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%doc CHANGES.md
%doc LICENSE
%doc README.md
%{_libdir}/ocaml/zed
%exclude %{_libdir}/ocaml/zed/*.a
%exclude %{_libdir}/ocaml/zed/*.cmxa
%exclude %{_libdir}/ocaml/zed/*.cmx
%exclude %{_libdir}/ocaml/zed/*.mli

%files devel
%{_libdir}/ocaml/zed/*.a
%{_libdir}/ocaml/zed/*.cmxa
%{_libdir}/ocaml/zed/*.cmx
%{_libdir}/ocaml/zed/*.mli

%changelog
* Tue Dec 9 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.3-2
- SCLify

* Thu Oct 2 2014 Euan Harris <euan.harris@citrix.com> - 1.3-1
- Update to 1.3 and switch to GitHub sources

* Mon Jun  2 2014 Euan Harris <euan.harris@citrix.com> - 1.2-2
- Split files correctly between base and devel packages

* Thu Jun  6 2013 David Scott <dave.scott@eu.citrix.com> - 1.2-1
- Initial package

