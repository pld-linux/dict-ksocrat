%define		dictname ksocrat
Summary:	English<->Russian dictionary for dictd
Summary(pl):	S³ownik angielsko<->rosyjski dla dictd
Name:		dict-%{dictname}
Version:	1.0.1
Release:	1
License:	for use with KSocrat only
Group:		Applications/Dictionaries
Source0:	http://webua.net/zavolzhsky/download/%{dictname}-enru-dic-%{version}.tar.bz2
# Source0-md5:	54dc44d886961d79dc677f62f9fc0b02
Source1:	http://webua.net/zavolzhsky/download/%{dictname}-ruen-dic-%{version}.tar.bz2
# Source1-md5:	a6b2a0b365b65e2ced72707b8dc1ad5f
URL:		http://webua.net/zavolzhsky/english/programs.html
Patch0:		%{dictname}-enru.patch
BuildRequires:	dictfmt
BuildRequires:	dictzip
Requires:	%{_sysconfdir}/dictd
Requires:	dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
English<->Russian dictionary for dictd encoded in koi8-r. Start server
with --locale ru_RU.KOI8-R option in order to use it.

%description -l pl
S³ownik angielsko<->rosyjski dla dictd kodowany w koi8-r. Uruchom
serwer z opcj± --locale ru_RU.KOI8-R, ¿eby móc go u¿ywaæ.

%package enru
Summary:	English-Russian dictionary for dictd
Summary(pl):	S³ownik angielsko-rosyjski dla dictd
Group:		Applications/Dictionaries

%description enru
English-Russian dictionary for dictd encoded in koi8-r.

%description enru -l pl
S³ownik angielsko-rosyjski dla dictd kodowany w koi8-r.

%package ruen
Summary:	Russian-English dictionary for dictd
Summary(pl):	S³ownik rosyjsko-angielski dla dictd
Group:		Applications/Dictionaries

%description ruen
Russian-English dictionary for dictd encoded in koi8-r. Start server
with --locale ru_RU.KOI8-R option in order to use it.

%description ruen -l pl
S³ownik rosyjsko-angielski dla dictd kodowany w koi8-r. Uruchom serwer
z opcj± --locale ru_RU.KOI8-R, ¿eby móc go u¿ywaæ.

%prep
%setup -q -c -a1
%patch0 -p0

%build
perl -pe 's/^(.*?)\s*--\s*(.*?)\s*$/:$1: - $2\n/' < usr/share/apps/ksocrat/enru.dic | \
	dictfmt -j -u http://webua.net/zavolzhsky/english/programs.html -s \
	"KSocrat English-Russian dictionary (%{version})" %{dictname}-enru

perl -pe 's/^(.*?)\s*--\s*(.*?)\s*$/:$1: - $2\n/' < usr/share/apps/ksocrat/ruen.dic | \
	dictfmt -j -u http://webua.net/zavolzhsky/english/programs.html -s \
	"KSocrat Russian-English dictionary (%{version})" %{dictname}-ruen --locale ru_RU.KOI8-R

dictzip %{dictname}*.dict

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd,%{_sysconfdir}/dictd}

dictprefix=%{_datadir}/dictd/%{dictname}-enru
echo "# KSocrat English-Russian dictionary
database %{dictname}-enru {
	data  \"$dictprefix.dict.dz\"
	index \"$dictprefix.index\"
}" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}-enru.dictconf

dictprefix=%{_datadir}/dictd/%{dictname}-ruen
echo "# KSocrat Russian-English dictionary
database %{dictname}-ruen {
	data  \"$dictprefix.dict.dz\"
	index \"$dictprefix.index\"
}" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}-ruen.dictconf
mv %{dictname}* $RPM_BUILD_ROOT%{_datadir}/dictd

%clean
rm -rf $RPM_BUILD_ROOT

%post enru
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%postun enru
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2 || true
fi

%post ruen
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%postun ruen
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2 || true
fi

%files enru
%defattr(644,root,root,755)
%doc usr/share/apps/ksocrat/*_ENG.txt
%lang(ru) %doc usr/share/apps/ksocrat/*_RUS.txt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dictd/%{dictname}-enru.dictconf
%{_datadir}/dictd/%{dictname}-enru.*

%files ruen
%defattr(644,root,root,755)
%doc usr/share/apps/ksocrat/*_ENG.txt
%lang(ru) %doc usr/share/apps/ksocrat/*_RUS.txt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dictd/%{dictname}-ruen.dictconf
%{_datadir}/dictd/%{dictname}-ruen.*
