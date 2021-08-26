%global galeradoc %{buildroot}%{_docdir}/galera
Name:           galera
Version:        26.4.8
Release:        1
Summary:        Synchronous multi-master replication library
License:        GPLv2
URL:            http://galeracluster.com/
Source0:        http://releases.galeracluster.com/%{name}-4.8/source/%{name}-4-%{version}.tar.gz
Source1:        garbd.service
#systemd startup script
Source2:        garbd-wrapper

#Use decode to make the SConstruct Python3 compatible
#https://github.com/codership/galera/commit/71685db8da72b81a0950c19269281d10ae179706.patch
Patch0000:      galera-python3.patch

BuildRequires:  asio-devel boost-devel check-devel gcc-c++ openssl-devel python3-scons systemd
Requires:       nmap-ncat

Requires(post,preun,postun):  systemd

%description
This is Galera replication - Codership's implementation of the write set replication (wsrep) interface.

%prep
%autosetup -n %{name}-4-%{version} -p1

sed -i '/^GALERA_VER/s/API + //' wsrep/tests/SConscript

%build
%{set_build_flags}

CPPFLAGS=`echo $CPPFLAGS| sed -e "s|-Wp,-D_GLIBCXX_ASSERTIONS||g" `
CFLAGS=`echo $CFLAGS| sed -e "s|-Wp,-D_GLIBCXX_ASSERTIONS||g" `
CXXFLAGS=`echo $CXXFLAGS| sed -e "s|-Wp,-D_GLIBCXX_ASSERTIONS||g" `
export CPPFLAGS CFLAGS CXXFLAGS

scons-3 %{?_smp_mflags} strict_build_flags=1

%install
install -D -m 644 COPYING                       %{galeradoc}/COPYING
install -D -m 644 asio/LICENSE_1_0.txt          %{galeradoc}/LICENSE.asio
install -D -m 644 scripts/packages/README       %{galeradoc}/README
install -D -m 644 scripts/packages/README-MySQL %{galeradoc}/README-MySQL
install -D -m 644 garb/files/garb.cnf           %{buildroot}%{_sysconfdir}/sysconfig/garb
install -D -m 644 %{SOURCE1}                    %{buildroot}%{_unitdir}/garbd.service
install -D -m 755 %{SOURCE2}                    %{buildroot}%{_sbindir}/garbd-wrapper
install -D -m 755 garb/garbd                    %{buildroot}%{_sbindir}/garbd
install -D -m 755 libgalera_smm.so              %{buildroot}%{_libdir}/galera/libgalera_smm.so

%post
/sbin/ldconfig
%systemd_post garbd.service

%preun
%systemd_preun garbd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart garbd.service

%files
%config(noreplace,missingok) %{_sysconfdir}/sysconfig/garb
%dir %{_docdir}/galera
%doc %{_docdir}/galera/*
%dir %{_libdir}/galera
%{_libdir}/galera/libgalera_smm.so
%{_sbindir}/garbd*
%{_unitdir}/garbd.service

%changelog
* Wed Aug 25 2021 lingsheng <lingsheng@huawei.com> - 26.4.8-1
- Update to 26.4.8

* Mon Aug 16 2021 lingsheng <lingsheng@huawei.com> - 25.3.26-5
- Remove unsupported reload option

* Wed Jul 21 2021 lingsheng <lingsheng@huawei.com> - 25.3.26-4
- Remove unnecessary buildrequire gdb

* Sat Mar 21 2020 songnannan <songnannan2@huawei.com> - 25.3.26-3
- add gdb in buildrequires

* Thu Mar 4 2020 zhouyihang<zhouyihang1@huawei.com> - 25.3.26-2
- Pakcage init
