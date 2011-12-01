Name:           nautilus-sendto
Version:        2.28.2
Release:        3%{?dist}
Summary:        Nautilus context menu for sending files

Group:          User Interface/Desktops
License:        GPLv2+
URL:            ftp://ftp.gnome.org/pub/gnome/sources/%{name}
Source0:        http://download.gnome.org/sources/%{name}/2.28/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# updated translations
# https://bugzilla.redhat.com/show_bug.cgi?id=589228
Patch0: nautilus-sendto-translations.patch

BuildRequires:  gtk2-devel
BuildRequires:  libglade2-devel
BuildRequires:  evolution-data-server-devel >= 1.9.1
BuildRequires:  libgnomeui-devel
BuildRequires:  nautilus-devel >= 2.5.4
BuildRequires:  gettext
BuildRequires:  perl-XML-Parser intltool
BuildRequires:  dbus-glib-devel >= 0.70

Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2

# For compat with old nautilus-sendto packaging
Provides: nautilus-sendto-gaim
Obsoletes: nautilus-sendto-bluetooth
Provides: nautilus-sendto-bluetooth

%description
The nautilus-sendto package provides a Nautilus context menu for
sending files via other desktop applications.  These functions are
implemented as plugins, so nautilus-sendto can be extended with
additional features.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
License:	LGPLv2+
Requires:	%{name} = %{version}-%{release}
Requires:	gtk-doc pkgconfig

%description devel
This package contains the libraries amd header files that are needed
for writing plugins for nautilus-sendto.

%prep
%setup -q
%patch0 -p1 -b .translations

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

find $RPM_BUILD_ROOT \( -name '*.a' -o -name '*.la' \) -exec rm -f {} \;
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
	%{_sysconfdir}/gconf/schemas/nst.schemas > /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/gconf/schemas/nst.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/gconf/schemas/nst.schemas > /dev/null || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog ChangeLog.pre-1.1.4.1 COPYING NEWS
%{_libdir}/nautilus/extensions-2.0/libnautilus-sendto.so
%dir %{_libdir}/nautilus-sendto
%dir %{_libdir}/nautilus-sendto/plugins
%{_libdir}/nautilus-sendto/plugins/*.so
%{_datadir}/nautilus-sendto
%{_bindir}/nautilus-sendto
%{_sysconfdir}/gconf/schemas/nst.schemas
%{_mandir}/man1/nautilus-sendto.1.gz

%files devel
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/nautilus-sendto/
%{_libdir}/pkgconfig/nautilus-sendto.pc
%{_includedir}/nautilus-sendto/nautilus-sendto-plugin.h

%changelog
* Fri May 14 2010 Matthias Clasen <mclasen@redhat.com> 2.28.2-3
- Updated translations
Resolves: #589228

* Thu Dec 17 2009 Bastien Nocera <bnocera@redhat.com> 2.28.2-2
- Remove the empathy and UPNP plugins
Related: rhbz#543948

* Tue Nov 17 2009 Bastien Nocera <bnocera@redhat.com> 2.28.2-1
- Update to 2.28.2
- Add devel sub-package
- Remove unneeded pidgin and gajim BRs

* Tue Nov 17 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-1
- Update to 2.28.1

* Mon Sep 21 2009 Bastien Nocera <bnocera@redhat.com> 2.28.0-1
- Update to 2.28.0

* Fri Sep 18 2009 Caolán McNamara <caolanm@redhat.com> - 1.1.7-3
- rebuild for dependencies

* Tue Sep  8 2009 Brian Pepple <bpepple@fedoraproject.org> - 1.1.7-2
- Rebuild for new Empathy.

* Wed Sep 02 2009 Bastien Nocera <bnocera@redhat.com> 1.1.7-1
- Update to 1.1.7

* Wed Aug 26 2009 Brian Pepple <bpepple@fedoraproject.org> - 1.1.6-3
- Rebuild for new Empathy.

* Thu Jul 30 2009 Bastien Nocera <bnocera@redhat.com> 1.1.6-2
- Rebuild for new empathy

* Wed Jul 29 2009 Bastien Nocera <bnocera@redhat.com> 1.1.6-1
- Update to 1.1.6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Bastien Nocera <bnocera@redhat.com> 1.1.5-4
- Update for new empathy API

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> 1.1.5-3
- Rebuild against newer empathy

* Tue May 05 2009 Bastien Nocera <bnocera@redhat.com> 1.1.5-2
- Disable the evolution plugin, it will be in Evo itself in 2.27.x
  See http://bugzilla.gnome.org/show_bug.cgi?id=579099

* Tue May 05 2009 Bastien Nocera <bnocera@redhat.com> 1.1.5-1.1
- Update to 1.1.5

* Tue Apr 28 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.4.1-2
- Build with gajim support (#497975)

* Mon Apr 20 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.4.1-1
- Update to 1.1.4.1

* Fri Apr 17 2009 Karsten Hopp <karsten@redhat.com> 1.1.4-1.1
- don't require pidgin-* on s390, s390x as that has ExcludeArch s390(x)

* Fri Apr 17 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.4-1
- Update to 1.1.4

* Fri Apr 03 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.3-1
- Update to 1.1.3

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> - 1.1.2-4
- Make build and run with current Empathy

* Wed Mar 04 2009 Warren Togami <wtogami@redhat.com> - 1.1.2-3
- rebuild for libempathy

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.2-1
- Update to 1.1.2

* Tue Feb 17 2009 Paul W. Frields <stickster@gmail.com> - 1.1.1-3
- Rebuild for dependencies

* Thu Feb 12 2009 - Caolán McNamara <caolanm@redhat.com> - 1.1.1-2
- rebuild for dependencies

* Sat Jan 10 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.1
- Update to 1.1.1
- Add UPNP and Empathy plugins

* Tue Sep 23 2008 - Bastien Nocera <bnocera@redhat.com> - 1.1.0
- Update to 1.1.0

* Wed Jul 23 2008 - Bastien Nocera <bnocera@redhat.com> - 1.0.1
- Update to 1.0.1

* Thu Jun 12 2008 - Bastien Nocera <bnocera@redhat.com> - 1.0.0
- Update to 1.0.0

* Wed May 14 2008 Matthias Clasen <mclasen@redhat.com> - 0.14.0-4
- Rebuild again

* Tue May 13 2008 - Bastien Nocera <bnocera@redhat.com> - 0.14.0-3
- Rebuild

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.14.0-2
- Fix source url

* Thu Mar 27 2008 - Bastien Nocera <bnocera@redhat.com> - 0.14.0-1
- Update to 0.14.0

* Thu Feb 07 2008 - Bastien Nocera <bnocera@redhat.com> - 0.13.2-1
- Update to 0.13.2

* Mon Jan 21 2008 - Bastien Nocera <bnocera@redhat.com> - 0.13.1-1
- Update to 0.13.1

* Sun Jan 20 2008 - Bastien Nocera <bnocera@redhat.com> - 0.13-1
- Update to 0.13

* Fri Dec 28 2007 Adel Gadllah <adel.gadllah@gmail.com> - 0.12-7
- Fix icq file transfers with pidgin RH #408511

* Wed Dec 26 2007 Matthias Clasen <mclasen@redhat.com> - 0.12-6
- Install the nautilus exension in the right spot

* Mon Nov 19 2007 Matthias Clasen <mclasen@redhat.com> - 0.12-5
- Fix the pidgin plugin to work with libpurple (#389121)

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 0.12-4
- Rebuild against new dbus-glib

* Wed Oct 10 2007 Matthias Clasen <mclasen@redhat.com> - 0.12-3
- Rebuild

* Mon Aug 13 2007 - Bastien Nocera <bnocera@redhat.com> - 0.12-2
- Fix the Thunderbird patch to apply properly

* Mon Aug 13 2007 - Bastien Nocera <bnocera@redhat.com> - 0.12-1
- Update to 0.12 and drop obsolete patches

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 0.10-5
- Update the license field

* Fri May 11 2007 Stu Tomlinson <stu@nosnilmot.com> - 0.10-4
- Update to work with pidgin

* Wed May  9 2007 Matthias Clasen <mclasen@redhat.com> - 0.10-3
- Fix a problem with dbus error handling  (#239588)

* Mon Apr 16 2007 Warren Togami <wtogami@redhat.com> - 0.10-2
- disable gaim dep temporarily during transition to pidgin

* Sun Mar 11 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10-1
- Update to 0.10, as 0.9 didn't compile

* Fri Mar 09 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9-1
- Update to 0.9
- Remove the bluetooth subpackage, it only depends on
  gbus-glib now

* Tue Jan 23 2007 Alexander Larsson <alexl@redhat.com> - 0.8-4
- Rebuild against new gaim (#223765)

* Wed Nov 15 2006 Matthias Clasen <mclasen@redhat.com> - 0.8-3
- Rebuild against new libbtctl

* Fri Oct 27 2006 Matthew Barnes <mbarnes@redhat.com> - 0.8-2
- Update BuildRequires for evolution-data-server-devel.
- Rebuild against evolution-data-server-1.9.1.

* Fri Oct 20 2006 Matthias Clasen <mclasen@redhat.com> - 0.8-1
- Upgrade to 0.8

* Sat Sep 16 2006 Matthias Clasen <mclasen@redhat.com> - 0.7-5
- Include Thunderbird support and make it work
- Add missing BRs

* Mon Aug 14 2006 Alexander Larsson <alexl@redhat.com> - 0.7-4
- Buildrequire nautilus-devel

* Thu Aug 10 2006 Alexander Larsson <alexl@redhat.com> - 0.7-3
- Make nautilus-sendto-bluetooth require gnome-bluetooth (#201908)

* Sat Aug 05 2006 Caolan McNamara <caolanm@redhat.com> - 0.7-2
- rebuild against new e-d-s

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.7-1.1
- rebuild

* Tue Jul 11 2006 Matthias Clasen  <mclasen@redhat.com> - 0.7-1
- Update to 0.7

* Wed Jun 14 2006 Alexander Larsson <alexl@redhat.com> - 0.5-4
- Rebuild again, hopefully fixing libbluetooth issue

* Mon Jun 12 2006 Alexander Larsson <alexl@redhat.com> - 0.5-3
- Rebuild for new libbluetooth soname

* Sat Jun 10 2006 Matthias Clasen <mclasen@redhat.com> 0.5-2
- Add missing BuildRequires

* Mon May 22 2006 Alexander Larsson <alexl@redhat.com> 0.5-1
- Update to 0.5
- Add libgnomeui-devel buildreq

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.4-7.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.4-7.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Jan 28 2006 David Malcolm <dmalcolm@redhat.com> 0.4-7
- rebuild for new e-d-s

* Tue Dec 20 2005 Alexander Larsson <alexl@redhat.com> 0.4-6
- Rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Alexander Larsson <alexl@redhat.com> - 0.4-5
- Build in Core
- Move gaim plugin into main package
- Fix up some build requirements
- No bluetooth on s390*

* Sat Oct  8 2005 Paul W. Frields <stickster@gmail.com> - 0.4-4
- Eliminate superfluous Requires

* Sat Oct  8 2005 Paul W. Frields <stickster@gmail.com> - 0.4-3
- Rearrange Requires and BuildRequires for subpackages
- Include default Evolution plugin in main package

* Fri Oct  7 2005 Paul W. Frields <stickster@gmail.com> - 0.4-2
- Use appropriate BuildRequires for nautilus and gaim

* Fri Oct  7 2005 Paul W. Frields <stickster@gmail.com> - 0.4-1
- Initial version
