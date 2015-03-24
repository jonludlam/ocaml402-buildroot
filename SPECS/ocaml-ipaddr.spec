# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-ipaddr}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocaml-ipaddr
Version:        2.5.0
Release:        1001%{?dist}
Summary:        Pure OCaml parsers and printers for IP addresses
License:        ISC
URL:            https://github.com/mirage/ocaml-ipaddr
Source0:        https://github.com/mirage/ocaml-ipaddr/archive/%{version}/ocaml-ipaddr-%{version}.tar.gz

BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-sexplib-devel
BuildRequires:  %{?scl_prefix}ocaml-camlp4

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
A library for manipulation of IP (and MAC) address representations

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ocaml-sexplib-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocaml-ipaddr-%{version}

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}

%install
mkdir -p %{buildroot}/%{_libdir}/ocaml
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%doc CHANGES
%doc README.md
%{_libdir}/ocaml/ipaddr
%exclude %{_libdir}/ocaml/ipaddr/*.a
%exclude %{_libdir}/ocaml/ipaddr/*.cmxa
%exclude %{_libdir}/ocaml/ipaddr/*.cmx
%exclude %{_libdir}/ocaml/ipaddr/*.ml
%exclude %{_libdir}/ocaml/ipaddr/*.mli

%files devel
%{_libdir}/ocaml/ipaddr/*.a
%{_libdir}/ocaml/ipaddr/*.cmx
%{_libdir}/ocaml/ipaddr/*.cmxa
%{_libdir}/ocaml/ipaddr/*.mli

%changelog
* Mon Mar 23 2015 Jon Ludlam <jonathan.ludlam@citrix.com> - 2.5.0-1001
- SCLify

* Sat Jul 19 2014 David Scott <dave.scott@citrix.com> - 2.5.0-1000
- Update to 2.5.0; override upstream package

* Tue Apr 1 2014 Euan Harris <euan.harris@citrix.com> - 2.4.0-1
- Initial package

