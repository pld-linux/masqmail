Summary:	An offline mail server with pop3 client support
Summary(pl):	Serwer pocztowy offline ze wsparciem dla pop3
Name:		masqmail
Version:	0.2.16
Release:	1
License:	GPL
Vendor:		Oliver Kurth <kurth@innominate.de>
Group:		Networking/Daemons
Source0:	http://masqmail.cx/masqmail/download/%{name}-%{version}.tar.gz
URL:		http://masqmail.cx/masqmail/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib-devel
Provides:	smtpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MasqMail is a mail server designed for hosts that do not have a
permanent internet connection eg. a home network or a single host at
home. It has special support for connections to different ISPs. It
replaces sendmail or other MTAs such as qmail or exim.

%description -l pl
MasqMail jest serwerem pocztowym zaprojektowanym dla maszyn nie
posiadaj±cych sta³ego dostêpu do Internetu, jak domowe sieci czy
pojedyncze komputery domowe. Wspiera po³±czenia z ró¿nymi ISP.
Zastêpuje sendmaila oraz inne MTA jak qmail czy exim.

%prep
%setup -q

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-user=mail \
	--with-group=mail \
	--with-logdir=/var/log
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name}/tpl,%{_bindir},%{_libdir},%{_sbindir},%{_mandir}/man{5,8},%{_var}/spool/%{name}/{input,lock,popuidl}}

install tpl/failmsg.tpl $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tpl
install examples/masqmail.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install src/mservdetect $RPM_BUILD_ROOT%{_bindir}
install src/masqmail $RPM_BUILD_ROOT%{_sbindir}
install docs/man/masqmail.*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install docs/man/masqmail.8 $RPM_BUILD_ROOT%{_mandir}/man8
install debian/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install debian/newaliases $RPM_BUILD_ROOT%{_bindir}
ln -s -f '../sbin/masqmail' $RPM_BUILD_ROOT%{_bindir}/mailq
ln -s -f '../sbin/masqmail' $RPM_BUILD_ROOT%{_libdir}/sendmail
ln -s -f './masqmail' $RPM_BUILD_ROOT%{_sbindir}/sendmail

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL NEWS README TODO examples/example.*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/sendmail
%attr(755,root,root) %{_sbindir}/sendmail
%attr(4755,root,root) %{_sbindir}/masqmail
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}/masqmail.conf
%{_mandir}/man[58]/*
%defattr(644,mail,mail,755)
%dir %{_sysconfdir}/%{name}/tpl
%config %{_sysconfdir}/%{name}/tpl/failmsg.tpl
%dir %{_var}/spool/%{name}
%dir %{_var}/spool/%{name}/input
%dir %{_var}/spool/%{name}/lock
%dir %{_var}/spool/%{name}/popuidl
