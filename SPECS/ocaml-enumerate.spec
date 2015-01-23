# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-enumerate}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}ocaml-enumerate
Version:        111.08.00
Release:        2%{?dist}
Summary:        Quotation expanders for enumerating finite types.

Group:          Development/Libraries
License:        Apache-2.0
URL:            https://ocaml.janestreet.com/
Source0:        https://github.com/janestreet/enumerate/archive/%{version}/ocaml-enumerate-%{version}.tar.gz

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
Quotation expanders for enumerating finite types.

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
%setup -q -n enumerate-%{version}

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure --prefix %{_prefix}
# --destdir %{buildroot}
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
%doc README.md
%doc LICENSE.txt
%doc THIRD-PARTY.txt
%doc INRIA-DISCLAIMER.txt
%doc INSTALL.txt
%{_libdir}/ocaml/enumerate
%exclude %{_libdir}/ocaml/enumerate/*.a
%exclude %{_libdir}/ocaml/enumerate/*.cmxa
%exclude %{_libdir}/ocaml/enumerate/*.cmx
%exclude %{_libdir}/ocaml/enumerate/*.mli

%files devel
%{_libdir}/ocaml/enumerate/*.a
%{_libdir}/ocaml/enumerate/*.cmxa
%{_libdir}/ocaml/enumerate/*.cmx
%{_libdir}/ocaml/enumerate/*.mli

%changelog
* Wed Dec 3 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 111.08.00-2
- SCLify

* Tue Oct 14 2014 David Scott <dave.scott@citrix.com> - 111.08.00-1
- Initial package

