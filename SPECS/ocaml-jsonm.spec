# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-jsonm}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

Name:           %{?scl_prefix}ocaml-jsonm
Version:        0.9.1
Release:        2%{?dist}
Summary:        Non-blocking streaming JSON codec for OCaml
License:        BSD
URL:            http://erratique.ch/software/jsonm
Source0:        https://github.com/dbuenzli/jsonm/archive/v%{version}/ocaml-jsonm-%{version}.tar.gz
Patch0:         ocaml-jsonm-setup.ml.patch
BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-uutf-devel

%description
Jsonm is a non-blocking streaming codec to decode and encode the JSON
data format. It can process JSON text without blocking on IO and
without a complete in-memory representation of the data.

The alternative "uncut" codec also processes whitespace and
(non-standard) JSON with JavaScript comments.

Jsonm is made of a single module and depends on [Uutf][1]. It is
distributed under the BSD3 license.

[1]: http://erratique.ch/software/uutf

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ocaml-uutf-devel

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n jsonm-%{version}
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
mkdir -p %{buildroot}/%{_bindir}
%{?scl:scl enable %{scl} "}
ocaml setup.ml -install
%{?scl:"}

%files
%doc CHANGES
%doc README
%{_libdir}/ocaml/jsonm
%exclude %{_libdir}/ocaml/jsonm/*.a
%exclude %{_libdir}/ocaml/jsonm/*.cmxa
%exclude %{_libdir}/ocaml/jsonm/*.cmx
%exclude %{_libdir}/ocaml/jsonm/*.mli
%{_bindir}/jsontrip
%{_bindir}/ocamltweets

%files devel
%{_libdir}/ocaml/jsonm/*.a
%{_libdir}/ocaml/jsonm/*.cmxa
%{_libdir}/ocaml/jsonm/*.cmx
%{_libdir}/ocaml/jsonm/*.mli

%changelog
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.1-2
- SCLify

* Thu Oct 16 2014 David Scott <dave.scott@citri.com> - 0.9.1-1
- Initial package
