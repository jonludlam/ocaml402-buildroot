%global scl jonludlam-ocaml4021
%{?scl:%scl_package ocaml-fieldslib}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} /usr/lib/rpm/ocaml-find-requires.sh -c
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}ocaml-fieldslib
Version:        109.20.00
Release:        2%{?dist}
Summary:        OCaml record fields as first class values

Group:          Development/Libraries
License:        LGPLv2+ with exceptions and BSD
URL:            https://ocaml.janestreet.com
Source0:        https://ocaml.janestreet.com/ocaml-core/%{version}/individual/fieldslib-%{version}.tar.gz

BuildRequires:  %{?scl_prefix}ocaml >= 4.00.0
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-type-conv

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
OCaml record fields as first class values

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}ocaml-camlp4-devel%{?_isa}
Requires:       %{?scl_prefix}ocaml-type-conv%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n fieldslib-%{version}

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}

%install
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%doc README.txt
%doc LICENSE.txt
%doc COPYRIGHT.txt
%doc THIRD-PARTY.txt
%doc INRIA-DISCLAIMER.txt
%doc INSTALL.txt
%{_libdir}/ocaml/fieldslib
%exclude %{_libdir}/ocaml/fieldslib/*.a
%exclude %{_libdir}/ocaml/fieldslib/*.cmxa
%exclude %{_libdir}/ocaml/fieldslib/*.cmx
%exclude %{_libdir}/ocaml/fieldslib/*.mli

%files devel
%{_libdir}/ocaml/fieldslib/*.a
%{_libdir}/ocaml/fieldslib/*.cmxa
%{_libdir}/ocaml/fieldslib/*.cmx
%{_libdir}/ocaml/fieldslib/*.mli

%changelog
* Wed Dec 3 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 109.20.00-2
- SCLify

* Tue May 6 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 109.20.00-1
- Initial package

