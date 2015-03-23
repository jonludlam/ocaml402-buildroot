# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocamlscript}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocamlscript
Version:        2.0.3
Release:        2%{?dist}
Summary:        OCamlscript is a tool which compiles OCaml scripts into native code, thus combining mthe flexibility of scripts and the speed provided by ocamlopt.
License:        Boost
URL:            http://mjambon.com/ocamlscript.html
Source0:        https://github.com/mjambon/ocamlscript/archive/v%{version}/ocamlscript-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-findlib

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif


%description
OCamlscript is a tool which compiles OCaml scripts into native code, thus combining mthe flexibility of scripts and the speed provided by ocamlopt.

%prep
%setup -q -n ocamlscript-%{version}

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 ocamlscript %{buildroot}%{_bindir}/ocamlscript

export OCAMLFIND_DESTDIR=%{buildroot}%{_libdir}/ocaml
mkdir -p ${OCAMLFIND_DESTDIR}
export OCAMLFIND_LDCONF=ignore
%{?scl:scl enable %{scl} "}
ocamlfind install ocamlscript META ocamlscript.cmi ocamlscript.cmo ocamlscript.cmx ocamlscript.o
%{?scl:"}

%files
%doc Changes
%doc README
%{_bindir}/ocamlscript
%{_libdir}/ocaml/ocamlscript
%{_libdir}/ocaml/ocamlscript/META
%{_libdir}/ocaml/ocamlscript/ocamlscript.cmi
%{_libdir}/ocaml/ocamlscript/ocamlscript.cmo
%{_libdir}/ocaml/ocamlscript/ocamlscript.cmx
%{_libdir}/ocaml/ocamlscript/ocamlscript.o

%changelog
* Mon Mar 23 2015 Jon Ludlam <jonathan.ludlam@citrix.com> - 2.0.3-2
- SCLify

* Sun Jul 20 2014 David Scott <dave.scott@citrix.com> - 2.0.3-1
- Initial package
