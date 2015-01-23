# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-cmdliner}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

# Note - these two lines backported from Fedora
%global ocaml_native_compiler aarch64 %{arm} %{ix86} ppc ppc64 ppc64le sparc sparcv9 x86_64
%global ocaml_natdynlink      aarch64 %{arm} %{ix86} ppc ppc64 ppc64le sparc sparcv9 x86_64


%ifarch %{ocaml_native_compiler}
%global native_compiler 1
%global native_option true
%else
%global native_compiler 0
%global native_option false
%endif

%ifarch %{ocaml_natdynlink}
%global natdynlink_option true
%global natdynlink_compiler 1
%else
%global natdynlink_option false
%global natdynlink_compiler 0
%endif



Name:           %{?scl_prefix}ocaml-cmdliner
Version:        0.9.6
Release:        3%{?dist}
Summary:        Declarative definition of command-line interfaces for OCaml
License:        BSD
URL:            http://erratique.ch/software/cmdliner
Source0:        http://erratique.ch/software/cmdliner/releases/cmdliner-%{version}.tbz
Patch0:         cmdliner-enable-debug
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc

%description
Cmdliner is an OCaml module for the declarative definition of command line
interfaces. It provides a simple and compositional mechanism to convert
command line arguments to OCaml values and pass them to your functions.
The module automatically handles syntax errors, help messages and UNIX
man page generation. It supports programs with single or multiple commands
(like darcs or git) and respects most of the POSIX and GNU conventions.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n cmdliner-%{version}
%patch0 -p1

%build
%{?scl:scl enable %{scl} "}
ocaml pkg/git.ml
ocaml pkg/build.ml native=%{native_option} native-dynlink=%{natdynlink_option}
%{?scl:"}

%install
mkdir -p %{buildroot}/%{_libdir}/ocaml/cmdliner
cp _build/src/*.{cmi,cma,mli} _build/pkg/META  %{buildroot}/%{_libdir}/ocaml/cmdliner
%if %{native_compiler}
cp _build/src/*.{a,cmx,cmxa} %{buildroot}/%{_libdir}/ocaml/cmdliner
%if %{natdynlink_compiler}
cp _build/src/*.cmxs %{buildroot}/%{_libdir}/ocaml/cmdliner
%endif
%endif

%files
# Nb. the following line will pick up the .cmxs if natdynlink is true.
%doc CHANGES.md
%doc README.md
%{_libdir}/ocaml/cmdliner
%if %{native_compiler}
%exclude %{_libdir}/ocaml/cmdliner/*.a
%exclude %{_libdir}/ocaml/cmdliner/*.cmxa
%exclude %{_libdir}/ocaml/cmdliner/*.cmx
%endif
%exclude %{_libdir}/ocaml/cmdliner/*.mli

%files devel
%if %{native_compiler}
%{_libdir}/ocaml/cmdliner/*.a
%{_libdir}/ocaml/cmdliner/*.cmx
%{_libdir}/ocaml/cmdliner/*.cmxa
%endif
%{_libdir}/ocaml/cmdliner/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.6-3
- SCLify

* Thu Dec 11 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.6-2
- Fix debuginfo package

* Wed Dec 10 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.6-1
- Update to 0.9.6

* Thu Jul 17 2014 David Scott <dave.scott@citrix.com> - 0.9.5-1
- Update to 0.9.5

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 0.9.3-3
- Split files correctly between base and devel packages

* Mon May 19 2014 Euan Harris <euan.harris@citrix.com> - 0.9.3-2
- Switch to GitHub mirror

* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.3-1
- Initial package

