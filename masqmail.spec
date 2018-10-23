Summary:	An offline mail server with pop3 client support
Summary(pl.UTF-8):	Serwer pocztowy offline ze wsparciem dla pop3
Name:		masqmail
Version:	0.3.4
Release:	1
License:	GPL
Group:		Networking/Daemons/SMTP
Source0:	http://ftp.debian.org/debian/pool/main/m/masqmail/%{name}_%{version}.orig.tar.gz
# Source0-md5:	551bd887c71d7b8f3bb149b617adb1b3
Source1:	%{name}.aliases
Source2:	%{name}.conf
Source3:	%{name}.default.route
URL:		http://packages.debian.org/masqmail
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	libident-devel
BuildRequires:	openssl-devel
Provides:	smtpdaemon
Obsoletes:	smtpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	 -fomit-frame-pointer
%define		_sysconfdir		/etc/mail

%description
MasqMail is a mail server designed for hosts that do not have a
permanent internet connection eg. a home network or a single host at
home. It has special support for connections to different ISPs. It
replaces sendmail or other MTAs such as qmail or exim.

%description -l pl.UTF-8
MasqMail jest serwerem pocztowym zaprojektowanym dla maszyn nie
posiadających stałego dostępu do Internetu, jak domowe sieci czy
pojedyncze komputery domowe. Wspiera połączenia z różnymi ISP.
Zastępuje sendmaila oraz inne MTA jak qmail czy exim.

%prep
%setup -q

%build
%configure \
	--%{!?debug:dis}%{?debug:en}able-debug \
	--with-confdir=%{_sysconfdir} \
	--enable-auth \
	--enable-maildir \
	--enable-ident \
	--enable-mserver \
	--with-libcrypto \
	--with-user=mail \
	--with-group=mail \
	--with-logdir=/var/log \
	--with-spooldir=/var/spool/masqmail
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_prefix}/lib} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_datadir}/masqmail/tpl,%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT/var/spool/masqmail/{input,lock,popuidl}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/aliases
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/default.route
install src/mservdetect $RPM_BUILD_ROOT%{_bindir}
install src/masqmail $RPM_BUILD_ROOT%{_sbindir}
install tpl/* $RPM_BUILD_ROOT%{_datadir}/masqmail/tpl
install man/masqmail.*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install man/masqmail.8 $RPM_BUILD_ROOT%{_mandir}/man8
ln -sf ../sbin/masqmail $RPM_BUILD_ROOT%{_bindir}/mailq
ln -sf ../sbin/masqmail $RPM_BUILD_ROOT/usr/lib/sendmail
ln -sf masqmail $RPM_BUILD_ROOT%{_sbindir}/sendmail

%triggerpostun -- %{name} < 0.2.20-4.1
if [ -f /etc/masqmail/masqmail.conf.rpmsave ]; then
	cp -f  %{_sysconfdir}/masqmail.conf{,.rpmnew}
	mv -f /etc/masqmail/masqmail.conf.rpmsave %{_sysconfdir}/masqmail.conf
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO examples/example.*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /usr/lib/sendmail
%attr(4755,root,root) %{_sbindir}/masqmail
%attr(755,root,root) %{_sbindir}/sendmail
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/masqmail.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/default.route
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/aliases
%dir %{_datadir}/masqmail
%dir %{_datadir}/masqmail/tpl
%{_datadir}/masqmail/tpl/*.tpl
%lang(de) %{_datadir}/masqmail/tpl/*.tpl.de
%lang(fr) %{_datadir}/masqmail/tpl/*.tpl.fr
%lang(it) %{_datadir}/masqmail/tpl/*.tpl.it
%{_mandir}/man[58]/*
%defattr(644,mail,mail,755)
%dir /var/spool/masqmail
%dir /var/spool/masqmail/input
%dir /var/spool/masqmail/lock
%dir /var/spool/masqmail/popuidl
