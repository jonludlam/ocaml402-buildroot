# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-omd}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}ocaml-omd
Version:        1.0.2
Release:        1%{?dist}
Summary:        A Markdown frontend in pure OCaml.
License:        ISC
URL:            https://github.com/ocaml/omd
Source0:        https://github.com/ocaml/omd/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         ocaml-omd-setup.ml.patch
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc

%description
This Markdown library is implemented using only pure OCaml (including
I/O operations provided by the standard OCaml compiler distribution).
OMD is meant to be as faithful as possible to the original Markdown.
Additionally, OMD implements a few Github markdown features, an
extension mechanism, and a few other features. Note that the opam
package installs both the OMD library and the command line tool `omd`.
Note that The library interface of 1.0.x is only partially compatible
with 0.9.x.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n omd-%{version}
%patch0 -p1

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

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%{_libdir}/ocaml/omd
%exclude %{_libdir}/ocaml/omd/*.a
%exclude %{_libdir}/ocaml/omd/*.cmxa
%exclude %{_libdir}/ocaml/omd/*.cmx
%exclude %{_libdir}/ocaml/omd/*.mli
%{_bindir}/omd
%{_bindir}/test_cow
%{_bindir}/test_spec

%files devel
%{_libdir}/ocaml/omd/*.a
%{_libdir}/ocaml/omd/*.cmxa
%{_libdir}/ocaml/omd/*.cmx
%{_libdir}/ocaml/omd/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.0.2-2
- SCLify

* Thu Oct 16 2014 David Scott <dave.scott@citrix.com> - 1.0.2-1
- Initial package
