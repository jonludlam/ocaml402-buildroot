# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocamlify}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:		%{?scl_prefix}ocamlify
Version:	0.0.2
Release:	2%{?dist}
Summary:	Create OCaml source code by including whole files into OCaml string or string list
License:	LGPL
URL:		http://forge.ocamlcore.org/projects/ocamlify/
Source0:	http://forge.ocamlcore.org/frs/download.php/1209/ocamlify-%{version}.tar.gz

BuildRequires:	%{?scl_prefix}ocaml >= 3.10.2
BuildRequires:	%{?scl_prefix}ocaml-findlib

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
Create OCaml source code by including whole files into OCaml string or
string list.

%prep
%setup -q -n %{pkg_name}-%{version}

%build
%{?scl:scl enable %{scl} "}
./configure --prefix %{_prefix} --destdir %{buildroot}
make
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%doc AUTHORS.txt 
%doc CHANGES.txt
%doc COPYING.txt 
%{_bindir}/ocamlify

%changelog
* Mon Dec 1 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.0.2-2
- SCLify

* Tue Mar 25 2014 Euan Harris <euan.harris@citrix.com> - 0.0.2-1
- Initial package

