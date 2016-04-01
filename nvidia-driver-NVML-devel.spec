%global         debug_package %{nil}
%global         __strip /bin/true

Name:           nvidia-driver-NVML-devel
Version:        352.79
Release:        1%{?dist}
Summary:        NVIDIA Management Library (NVML) development files
Epoch:          1
License:        NVIDIA License
URL:            https://developer.nvidia.com/nvidia-management-library-nvml
Source0:        http://developer.download.nvidia.com/compute/cuda/7.5/Prod/gdk/gdk_linux_amd64_352_79_release.run

# The unversioned shared object is in the main driver development package
Requires:       nvidia-driver-NVML%{?_isa}
Obsoletes:      gpu-deployment-kit%{?_isa} < %{?epoch}:%{version}-%{release}
Provides:       gpu-deployment-kit%{?_isa} = %{?epoch}:%{version}-%{release}

%description
A C-based API for monitoring and managing various states of the NVIDIA GPU
devices. It provides a direct access to the queries and commands exposed via
nvidia-smi. The run-time version of NVML ships with the NVIDIA display driver,
and the SDK provides the appropriate header, stub libraries and sample
applications. Each new version of NVML is backwards compatible and is intended
to be a platform for building 3rd party applications.

%package -n nvidia-healthmon
Summary:        NVIDIA Tesla Health Monitor

%description -n nvidia-healthmon
System administrator's and cluster manager's tool for detecting and
troubleshooting common problems affecting NVIDIA Tesla GPUs in a high
performance computing environment. It contains limited hardware diagnostic
capabilities, and focuses on software and system configuration issues.

%package -n nvidia-validation-suite
Summary:        NVIDIA Validation Suite

%description -n nvidia-validation-suite
The NVIDIA Validation Suite (NVVS) is the system administrator and cluster
manager's tool for detecting and troubleshooting common problems affecting
NVIDIA Tesla GPUs in a high performance computing environments. NVVS focuses on
software and system configuration issues, diagnostics, topological concerns, and
relative performance.

%prep
%setup -c -T -n %{name}-%{version}
sh %{SOURCE0} --installdir=`pwd` --silent 

%install
# Man pages
mkdir -p %{buildroot}%{_mandir}/man3
cp -f .%{_mandir}/man3/* %{buildroot}%{_mandir}/man3/

# Headers
mkdir -p %{buildroot}%{_includedir}/nvidia/gdk
cp -f .%{_includedir}/nvidia/gdk/* %{buildroot}%{_includedir}/nvidia/gdk/

# Unversioned library (actual library comes from nvidia-driver)
mkdir -p %{buildroot}%{_libdir}
ln -s libnvidia-ml.so.1 %{buildroot}%{_libdir}/libnvidia-ml.so  

%ifarch x86_64
mkdir -p %{buildroot}%{_bindir} \
    %{buildroot}%{_libdir}/nvidia-validation-suite \
    %{buildroot}%{_mandir}/man8 \
    %{buildroot}%{_sysconfdir}

cp -fv .%{_mandir}/man8/* %{buildroot}%{_mandir}/man8/
cp -fr .%{_sysconfdir}/* %{buildroot}%{_sysconfdir}/

cp -fr .%{_bindir}/nvidia-healthmon* \
    %{buildroot}%{_bindir}/

cp -fr .%{_datadir}/nvidia-validation-suite/{nvvs,nvidia-vs,plugins} \
    %{buildroot}%{_libdir}/nvidia-validation-suite/

ln -sf %{_libdir}/nvidia-validation-suite/nvvs %{buildroot}%{_bindir}/nvvs 
%endif

%files
%doc usr/src/gdk/nvml/examples
%{_includedir}/nvidia/gdk
%{_libdir}/*.so
%{_mandir}/man3/*.3.*

%ifarch x86_64
%files -n nvidia-healthmon
%doc .%{_usrsrc}/gdk/README_HEALTHMON_DEPRECATED.txt
%dir %{_sysconfdir}/nvidia-healthmon/
%config(noreplace) %{_sysconfdir}/nvidia-healthmon/nvidia-healthmon.conf
%{_bindir}/nvidia-healthmon
# Find a way to move them out of here:
%{_bindir}/nvidia-healthmon-tests
%{_mandir}/man8/nvidia-healthmon.*

%files -n nvidia-validation-suite
%doc .%{_datadir}/nvidia-validation-suite/docs/NVIDIA_Validation_Suite_User_Guide.pdf
%doc .%{_datadir}/nvidia-validation-suite/*_examples
%dir %{_sysconfdir}/nvidia-validation-suite/
%config(noreplace) %{_sysconfdir}/nvidia-validation-suite/nvvs.conf
%{_bindir}/nvvs
%{_libdir}/nvidia-validation-suite
%{_mandir}/man8/nvvs.8.*
%endif

%changelog
* Sun Feb 14 2016 Simone Caronni <negativo17@gmail.com> - 1:352.79-1
- Update to 352.79.

* Tue Nov 10 2015 Simone Caronni <negativo17@gmail.com> - 1:352.55-1
- Update to 352.55.

* Thu Oct 01 2015 Simone Caronni <negativo17@gmail.com> - 1:352.39-2
- Fix binary symlink.

* Fri Sep 18 2015 Simone Caronni <negativo17@gmail.com> - 1:352.39-1
- Update to 352.39, new validation suite subpackage.

* Tue Sep 08 2015 Simone Caronni <negativo17@gmail.com> - 1:346.46-4
- Update isa requirements.

* Wed Aug 12 2015 Simone Caronni <negativo17@gmail.com> - 1:346.46-3
- Switch requirements to separate nvidia-driver-NVML package.
- Move unversioned libnvidia-ml link here from the main nvidia-driver-libs
  package.

* Tue Aug 04 2015 Simone Caronni <negativo17@gmail.com> - 1:346.46-2
- Add dependency on nvidia-driver-devel.

* Fri Mar 27 2015 Simone Caronni <negativo17@gmail.com> - 1:346.46-1
- Update to 346.46.
- Package nvidia-healthmon only on x86_64, no longer available in 32 bit form.

* Wed Sep 24 2014 Simone Caronni <negativo17@gmail.com> - 1:340.29-1
- Update to 340.29.

* Wed Aug 20 2014 Simone Caronni <negativo17@gmail.com> - 1:340.21-1
- Update to 340.21.
- Package nvidia-healthmon is now available also on 32 bit.

* Mon Jul 14 2014 Simone Caronni <negativo17@gmail.com> - 1:331.62-1
- First build.
- Create nvidia-healthmon subpackage (x86_64 only).
