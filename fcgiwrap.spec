%define systemd_test_str %(
if [[ -z $(pkg-config --print-errors libsystemd-daemon 2>&1) ]]; then
  echo "yes"
else
  echo "no"
fi
)
%if "%{systemd_test_str}" == "yes"
    %define with_systemd 1
%endif

Name:		fcgiwrap
Version:	1.1.0
Release:	1%{?dist}
Summary:	Simple FastCGI wrapper for CGI scripts
Group:		System Environment/Daemons
License:	BSD-like
URL:		http://nginx.localdomain.pl/wiki/FcgiWrap
Source0:	%{name}-%{version}.tgz
BuildRequires:	autoconf automake fcgi-devel pkgconfig
%{?with_systemd:BuildRequires:  systemd-devel systemd}
Requires:	fcgi

%description
This package provides a simple FastCGI wrapper for CGI scripts with/
following features:
 - very lightweight (84KB of private memory per instance)
 - fixes broken CR/LF in headers
 - handles environment in a sane way (CGI scripts get HTTP-related env.
   vars from FastCGI parameters and inherit all the others from
   environment of fcgiwrap )
 - no configuration, so you can run several sites off the same
   fcgiwrap pool
 - passes CGI stderr output to stderr stream of cgiwrap or FastCGI


%prep
%setup -q

%build
autoreconf -i
%configure

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sbindir}/fcgiwrap
#TODO: figure out why the manpage file is compressed automatically
%doc %{_mandir}/man8/fcgiwrap.8.gz
%{?with_systemd:
    %{_unitdir}/*.service
    %{_unitdir}/*.socket
}
%changelog
* Tue Apr 22 2014 Justin Zhang <schnell18[AT]gmail.com> - 1.1.0-1
- version 1.1.0
- First spec file for the fcgiwrap