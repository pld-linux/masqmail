Summary:	An offline mail server with pop3 client support
Summary(pl):	Serwer pocztowy offline ze wsparciem dla pop3
Name:		masqmail
Version:	0.2.20
Release:	1
License:	GPL
Group:		Networking/Daemons
# Source0-md5:	74540980ecde45783e888d1da80cb318
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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/masqmail,%{_bindir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_datadir}/masqmail/tpl,%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT%{_var}/spool/masqmail/{input,lock,popuidl}

install examples/masqmail.conf $RPM_BUILD_ROOT%{_sysconfdir}/masqmail
install src/mservdetect $RPM_BUILD_ROOT%{_bindir}
install src/masqmail $RPM_BUILD_ROOT%{_sbindir}
install tpl/* $RPM_BUILD_ROOT%{_datadir}/masqmail/tpl
install docs/man/masqmail.*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install docs/man/masqmail.8 $RPM_BUILD_ROOT%{_mandir}/man8
install debian/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install debian/newaliases $RPM_BUILD_ROOT%{_bindir}
ln -sf ../sbin/masqmail $RPM_BUILD_ROOT%{_bindir}/mailq
ln -sf ../sbin/masqmail $RPM_BUILD_ROOT%{_libdir}/sendmail
ln -sf masqmail $RPM_BUILD_ROOT%{_sbindir}/sendmail

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO examples/example.*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*
%attr(4755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/masqmail
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/masqmail/masqmail.conf
%dir %{_datadir}/masqmail
%dir %{_datadir}/masqmail/tpl
%{_datadir}/masqmail/tpl/*.tpl
%lang(de) %{_datadir}/masqmail/tpl/*.tpl.de
%lang(fr) %{_datadir}/masqmail/tpl/*.tpl.fr
%lang(it) %{_datadir}/masqmail/tpl/*.tpl.it
%{_mandir}/man[58]/*
%defattr(644,mail,mail,755)
%dir %{_var}/spool/masqmail
%dir %{_var}/spool/masqmail/input
%dir %{_var}/spool/masqmail/lock
%dir %{_var}/spool/masqmail/popuidl
