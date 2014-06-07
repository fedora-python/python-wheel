# Created by pyp2rpm-1.0.1
%global pypi_name wheel

Name:           python35-%{pypi_name}
Version:        0.24.0
Release:        0.2.20140607hg79e669d9f170%{?dist}
Summary:        A built-package format for Python

License:        MIT
URL:            http://bitbucket.org/dholth/wheel/
Source0:        python3-nightly-wheel-79e669d9f170.tar
BuildArch:      noarch

BuildRequires:  python35-devel
BuildRequires:  python35-setuptools

%description
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.

This is package contains Python 3 version of the package.

%prep
%setup -q -n python3-nightly-%{pypi_name}

# header files just has to be there, even empty
touch %{pypi_name}/test/headers.dist/header.h

# remove unneeded shebangs
sed -ie '1d' %{pypi_name}/{egg2wheel,wininst2wheel}.py


%build
%{__python35} setup.py build


%install
%{__python35} setup.py install --skip-build --root %{buildroot}

pushd %{buildroot}%{_bindir}
for f in $(ls); do mv $f python35-$f; done
popd


%files
%doc LICENSE.txt CHANGES.txt README.txt
%{_bindir}/python35-egg2wheel
%{_bindir}/python35-wheel
%{_bindir}/python35-wininst2wheel
%{python35_sitelib}/%{pypi_name}*
%exclude %{python35_sitelib}/%{pypi_name}/test


%changelog
* Sat Jun 07 2014 Miro Hrončok <mhroncok@redhat.com> - 0.24.0-0.2.20140607hg79e669d9f170
- Remove already merged patches

* Sat Jun 07 2014 Miro Hrončok <mhroncok@redhat.com> - 0.24.0-0.1.20140607hg79e669d9f170
- Update to hg: 79e669d9f170

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-3
- Another rebuild with python 3.4

* Fri Apr 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-2
- Rebuild with python 3.4

* Thu Nov 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.22.0-1
- Initial package.
