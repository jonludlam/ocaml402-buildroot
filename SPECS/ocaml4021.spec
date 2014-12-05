# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml4021 in this case
%global scl ocaml4021
%endif
%scl_package %scl

%global install_scl 1

Name: %scl_name
Version: 1
Release: 2%{?dist}
Summary: Package that installs %scl	
License: GPLv2+

BuildRequires: scl-utils-build	
Requires: %{scl_prefix}ocaml	

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build
Requires: scl-utils

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%prep
%setup -c -T

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_scl_scripts}/root

%scl_install

cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\$MANPATH
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}
export CAML_LD_LIBRARY_PATH=%{_libdir}/ocaml/stublibs
export OCAML_TOPLEVEL_PATH=%{_libdir}/ocaml/toplevel
EOF

%files

%files runtime
%scl_files

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Fri Nov 28 2014 Jon Ludlam <jonathan.ludlam@citrix.com> 1-2
- Add scl-utils to -build's requires

* Fri Nov 21 2014 Jon Ludlam <jonathan.ludlam@citrix.com> 1-1
- Initial package
