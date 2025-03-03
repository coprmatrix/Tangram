#
# spec file for package Tangram
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           Tangram
Version:        3.0
Release:        0
Summary:        Run web apps on your desktop
License:        GPL-3.0-or-later
URL:            https://github.com/sonnyp/Tangram
Source:         Tangram-%{version}.tar.gz
BuildRequires:  meson
BuildRequires:  (ninja or ninja-build)
BuildRequires:  (gtk4-tools or gtk4-devel-tools)
%define alternatives (alternatives or update-alternatives)
BuildRequires:  make
BuildRequires:  git
BuildRequires:  unzip
BuildRequires:  desktop-file-utils
BuildRequires:  python3-gobject
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gjs-1.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(blueprint-compiler)
BuildRequires:  pkgconfig(webkitgtk-6.0)
BuildRequires:  pkgconfig(libadwaita-1)
BuildArch:      noarch

%if 0%{?suse_version}
%define typelib() typelib(%{1}) = %{2}
%else
%define typelib() %{_libdir}/girepository-1.0/%{1}-%{2}.typelib
%endif

Requires:       %{typelib WebKit 6.0}
Requires:       %{typelib Adw 1}
Requires:       %{typelib Gtk 4.0}
Requires:       %{typelib Soup 3.0}
Requires:       %{typelib Gst 1.0}
Requires:       %{typelib GLib 2.0}
Requires:       %{typelib Gio 2.0}
Requires:       %{typelib Gdk 4.0}

Provides:       tangram


Requires(post):    %alternatives
Requires(postun):  %alternatives

%description
%{summary}.

%package lang
Version: %{version}
Summary: Language modes

%description lang
%{summary}.

%prep
%autosetup

sed -i 's|../blueprint-compiler/blueprint-compiler.py|/usr/bin/blueprint-compiler|g' src/meson.build

%build
%meson
%meson_build

%install
%meson_install
rm -R '%{buildroot}%{_datadir}/locale/ru*' || :

%files
%license COPYING
%doc README.md TODO.md
%{_bindir}/re.sonny.Tangram
%{_datadir}/re.sonny.Tangram/
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1
%{_datadir}/dbus-1/services/*.service
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor
%{_datadir}/icons/hicolor/*/*/*.svg
%{_datadir}/metainfo/*.metainfo.xml

%files lang
%{_datadir}/locale/**/*


%post
#!/bin/sh
echo post install "$1"
if [ "$1" == 1 ]; then
   %{_sbindir}/update-alternatives --install '%{_bindir}/tangram' tangram '%{_bindir}/re.sonny.Tangram' 25
fi

%postun
#!/bin/sh
echo post remove "$1"
if [ "$1" == 0 ]; then
   %{_sbindir}/update-alternatives --remove tangram '%{_bindir}/re.sonny.Tangram' || : 
fi

%changelog

