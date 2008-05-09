#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		rel	0.1
Summary:	Linux ABI modules
Name:		linux-abi
Version:	0.1
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/linux-abi/IBCS-3_6.TGZ
# Source0-md5:	7f9f908e79ae14eb7405c6d591467cb0
URL:		http://sourceforge.net/project/showfiles.php?group_id=13130
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux ABI is a patch to the Linux kernel that allows a Linux
system to run foreign binaries.

%package -n kernel%{_alt_kernel}-misc-abi
Summary:	Linux modules that allow to run foreign binaries
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-abi
The Linux ABI is a patch to the Linux kernel that allows a Linux
system to run foreign binaries.

This package contains Linux modules.

%prep
%setup -qc

%build
%if %{with kernel}
%build_kernel_modules ABI_DIR=$PWD ABI_VER=%(uname -r) -m all
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%endif

%if %{with kernel}
%install_kernel_modules -m all -d kernel/misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-abi
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-abi
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-abi
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/misc/*.ko*
%endif

%if %{with userspace}
%files
%defattr(644,root,root,755)

%endif
