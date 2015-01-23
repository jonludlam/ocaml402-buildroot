# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-re}
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
%else
%global native_compiler 0
%endif

Name:           %{?scl_prefix}ocaml-re
Version:        1.2.2
Release:        3%{?dist}
Summary:        A regular expression library for OCaml

License:        LGPLv2 with exceptions
URL:            https://github.com/ocaml/ocaml-re
Source0:        https://github.com/ocaml/ocaml-re/archive/ocaml-re-%{version}/ocaml-re-%{version}.tar.gz
# Without this, the re_pcre.ml file was installed. The problem is already fixed in master.
Patch0:         ocaml-re-add-pcre-mli

BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc

%description 

A pure OCaml regular expression library. Supports Perl-style regular
expressions, Posix extended regular expressions, Emacs-style regular
expressions, and shell-style file globbing.  It is also possible to
build regular expressions by combining simpler regular expressions.
There is also a subset of the PCRE interface available in the Re.pcre
library.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocaml-re-ocaml-re-%{version}
%patch0 -p1

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure --destdir $RPM_BUILD_ROOT
make
%{?scl:"}

%install
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%doc CHANGES
%doc LICENSE
%doc README.md
%{_libdir}/ocaml/re
%if %{native_compiler}
%exclude %{_libdir}/ocaml/re/*.a
%exclude %{_libdir}/ocaml/re/*.cmxa
%exclude %{_libdir}/ocaml/re/*.cmx
%endif
%exclude %{_libdir}/ocaml/re/*.mli

%files devel
%doc re-api.docdir/*
%exclude /usr/local/share/doc/re/
%if %{native_compiler}
%{_libdir}/ocaml/re/*.a
%{_libdir}/ocaml/re/*.cmx
%{_libdir}/ocaml/re/*.cmxa
%endif
%{_libdir}/ocaml/re/*.mli

%changelog 
* Sun Dec 14 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.2.2-3
- SCLify

* Fri Dec 12 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.2.2-2 
- Minor updates to the SPEC file. Now rpmlint gives no errors.

* Sat Jun  7 2014 David Scott <dave.scott@citrix.com> - 1.2.2-1
- Update to 1.2.2

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 1.2.1-2
- Split files correctly between base and devel packages

* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com> - 1.2.1-1
- Initial package

