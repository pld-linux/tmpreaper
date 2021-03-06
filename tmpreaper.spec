# TODO:
# - use /etc/tmpwatch dir and obsolete tmpwatch?

# NOTE
# - fork discussion: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=71251

Summary:	A utility for removing files based on when they were last accessed
Summary(de.UTF-8):	Utility zum Entfernen von Dateien, basierend auf ihrer Zugriffszeit
Summary(es.UTF-8):	Limpia archivos en directorios basado en sus edades
Summary(fr.UTF-8):	Nettoie les fichiers dans les répertoires en fonction de leur age
Summary(pl.UTF-8):	Narzędzie kasujące pliki w oparciu o czas ostatniego dostępu
Summary(pt_BR.UTF-8):	Limpa arquivos em diretórios baseado em suas idades
Summary(ru.UTF-8):	Утилита удаления файлов по критерию давности последнего доступа
Summary(uk.UTF-8):	Утиліта видалення файлів за критерієм давності останнього доступу
Name:		tmpreaper
Version:	1.6.13
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://ftp.debian.org/debian/pool/main/t/tmpreaper/%{name}_%{version}+nmu1.tar.gz
# Source0-md5:	36bffb38fbdd28b9de8af229faabf5fe
Source1:	%{name}.sysconfig
Source2:	%{name}.cron
Source3:	%{name}.conf
Source4:	%{name}.crontab
Source5:	cronjob-%{name}.timer
Source6:	cronjob-%{name}.service
URL:		http://packages.debian.org/sid/tmpreaper
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.644
Requires:	systemd-units >= 38
Suggests:	cronjobs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The tmpreaper utility recursively searches through specified
directories and removes files which have not been accessed in a
specified period of time. tmpreaper is normally used to clean up
directories which are used for temporarily holding files (for example,
/tmp). tmpreaper ignores symlinks, won't switch filesystems and only
removes empty directories and regular files.

%description -l de.UTF-8
Das tmpreaper-Utility sucht rekursiv durch angegebene Verzeichnisse
und entfernt Dateien, die in einer angegebenen Zeitspanne nicht
benutzt wurden. tmpreaper wird normalerweise benutzt, um Verzeichnisse
aufzuräumen, in denen temporäre Dateien gelagert werden (z.B. /tmp).
tmpreaper ignoriert symlinks, wechselt kein Filesystem und entfernt
nur normale Dateien und leere Verzeichnisse.

%description -l es.UTF-8
Este paquete nos ofrece un programa que puede ser usado para limpiar
directorios. Periódicamente remueve el directorio (ignorando symlinks)
y elimina archivos que no fueron accedidos en un tiempo especificado
por el usuario.

%description -l fr.UTF-8
Ce paquetage offre un programme permettant de nettoyer les
répertoires. Il recherche récursivement dans le répertoire (en
ignorant les liens symboliques) et supprime les fichiers qui n'ont pas
été accédés depuis une période donnée.

%description -l pl.UTF-8
tmpreaper rekursywnie przeszukuje wyspecyfikowane katalogi szukając
plików, które nie były używane przez określony okres czasu, w celu ich
usunięcia. Jest on zazwyczaj używany do czyszczenia katalogów w
których przechowywane są pliki tymczasowe (na przykład /tmp).
tmpreaper ignoruje symlinki, nie zmienia systemu plików podczas
przeszukiwania katalogów, usuwa tylko puste katalogi i zwyczajne
pliki.

%description -l pt_BR.UTF-8
Este pacote oferece um programa que pode ser usado para limpar
diretórios. Ele periodicamente vasculha o diretório (ignorando
symlinks) e remove arquivos que não foram acessados em um tempo
especificado pelo usuário.

%description -l tr.UTF-8
Bu paket, dizinleri temizleyen bir program içerir. Simgesel bağları
gözönüne almadan dizinleri rekürsif olarak arar ve kullanıcının
önceden belirlediği bir sürede erişilmemiş olanları siler.

%description -l ru.UTF-8
Утилита tmpreaper рекурсивно удаляет в указанных каталогах файлы, к
которым не было доступа указанное время. Обычно используется для
очистки каталогов, хранящих временные файлы (например, /tmp). Эта
утилита игнорирует симлинки, не переходит на другие файловые системы и
удаляет только пустые каталоги и обычные (не специальные) файлы.

%description -l uk.UTF-8
Утиліта tmpreaper рекурсивно видаляє у вказаних каталогах файли, до
яких не було доступу вказаний час. Звичайно використовується для
очистки каталогів, що зберігають тимчасові файли (наприклад, /tmp). Ця
утиліта ігнорує симлінки, не переходить на інші файлові системи і
видаляє тільки порожні каталоги та звичайні (не спеціальні) файли.

%prep
%setup -qc
mv tmpreaper-%{version}*/* .

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--sbindir=%{_bindir} \
	--with-fuser=/bin/fuser
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,sysconfig,%{name}},%{_prefix}/lib,%{_sbindir},%{systemdunitdir}}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/cron.d/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/tmpreaper/common.conf
install -p %{SOURCE2} $RPM_BUILD_ROOT%{_prefix}/lib/tmpreaper

cp -p %{SOURCE5} %{SOURCE6} $RPM_BUILD_ROOT%{systemdunitdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post cronjob-%{name}.timer

%preun
%systemd_preun cronjob-%{name}.timer

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/tmpreaper
%attr(755,root,root) %{_prefix}/lib/tmpreaper
%dir %{_sysconfdir}/tmpreaper
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tmpreaper/*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/tmpreaper
%{_mandir}/man8/tmpreaper.8*
%{systemdunitdir}/cronjob-%{name}.service
%{systemdunitdir}/cronjob-%{name}.timer
