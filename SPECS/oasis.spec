# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package oasis}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:		%{?scl_prefix}oasis
Version:	0.4.4
Release:	2%{?dist}
Summary:	Architecture for building OCaml libraries and applications

License:	LGPL
URL:		http://oasis.forge.ocamlcore.org/index.html
Source0:	https://github.com/ocaml/oasis/archive/%{version}/oasis-%{version}.tar.gz

BuildRequires:	%{?scl_prefix}ocaml
BuildRequires:	%{?scl_prefix}ocaml-camlp4-devel
BuildRequires:	%{?scl_prefix}ocaml-findlib-devel
BuildRequires:	%{?scl_prefix}ocamlify
BuildRequires:	%{?scl_prefix}ocamlmod
BuildRequires:	%{?scl_prefix}ocaml-ocamldoc
BuildRequires:	%{?scl_prefix}ocaml-odn-devel

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
OASIS generates a full configure, build and install system for your
application. It starts with a simple `_oasis` file at the toplevel of
your project and creates everything required.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}ocaml-odn-devel%{?_isa}

%description    devel
The %{pkg_name}-devel package contains libraries and signature files for
developing applications that use %{pkg_name}.

# The auto-requirements script mistakenly thinks that the Oasis library
# modules depend on OASISAstTypes.
%{?filter_setup:
%filter_from_requires /OASISAstTypes/d
%filter_setup
}

%prep
%setup -q -n oasis-%{version}


%build
%{?scl:scl enable %{scl} "}
./configure --prefix %{_prefix} --destdir %{buildroot}
make
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p \$OCAMLFIND_DESTDIR
make install
%{?scl:"}


%files
%{_bindir}/oasis

%{_libdir}/ocaml/plugin-loader/META
%{_libdir}/ocaml/plugin-loader/*.cma
%{_libdir}/ocaml/plugin-loader/*.cmi

%{_libdir}/ocaml/oasis/META
%{_libdir}/ocaml/oasis/*.cma
%{_libdir}/ocaml/oasis/*.cmi
%{_libdir}/ocaml/oasis/*.mli

%{_libdir}/ocaml/userconf/META
%{_libdir}/ocaml/userconf/*.cma
%{_libdir}/ocaml/userconf/*.cmi



%files devel
%{_libdir}/ocaml/plugin-loader/*.a
%{_libdir}/ocaml/plugin-loader/*.cmx
%{_libdir}/ocaml/plugin-loader/*.cmxa
%exclude %{_libdir}/ocaml/plugin-loader/*.cmxs
%exclude %{_libdir}/ocaml/plugin-loader/*.ml

%{_libdir}/ocaml/oasis/*.a
%{_libdir}/ocaml/oasis/*.cmx
%{_libdir}/ocaml/oasis/*.cmxa
%exclude %{_libdir}/ocaml/oasis/*.cmxs
%exclude %{_libdir}/ocaml/oasis/*.ml

%{_libdir}/ocaml/userconf/*.a
%{_libdir}/ocaml/userconf/*.cmx
%{_libdir}/ocaml/userconf/*.cmxa
%exclude %{_libdir}/ocaml/userconf/*.cmxs
%exclude %{_libdir}/ocaml/userconf/*.ml


%changelog
* Tue Dec 2 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.4.4-2
- SCLify

* Wed Mar 26 2014 Euan Harris <euan.harris@citrix.com> - 0.4.4-1
- Initial package

